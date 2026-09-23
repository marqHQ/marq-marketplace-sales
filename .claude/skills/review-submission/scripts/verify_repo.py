#!/usr/bin/env python3
"""Run the repository's deterministic checks and write a markdown report.

The review workflow runs this AFTER the model has reviewed a proposal, so the
pull-request body carries evidence the model did not produce: test suites,
manifest validation, manifest sync and version bump, README catalog, and the
new skill's package shape. Exit 0 when every check passes, 1 otherwise.

    python3 verify_repo.py --skill <name> --out .intake/verify.md [--base-ref origin/main] [--removed]

--removed is for feedback that deletes a skill: it checks the folder and every
README mention are gone instead of checking the skill's package shape.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PLUGIN = ROOT / "plugins" / "marq-sales-suite"
SKILLS = PLUGIN / "skills"
CLAUDE_MANIFEST = PLUGIN / ".claude-plugin" / "plugin.json"
CODEX_MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"

TEST_COMMANDS = [
    "plugins/marq-sales-suite/skills/audit-hubspot-pipeline/scripts/run_tests.py",
    "plugins/marq-sales-suite/skills/marq-deal-acceleration/scripts/run_tests.py",
    "plugins/marq-sales-suite/skills/marq-post-call-execution/scripts/check_acceptance_fixtures.py",
    ".claude/skills/review-submission/scripts/test_unpack_submission.py",
]
NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty".split())}
LINK = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:)([^)#]+)(?:#[^)]*)?\)")


class Report:
    def __init__(self) -> None:
        self.lines: list[str] = ["## Deterministic verification", ""]
        self.failed = 0

    def check(self, title: str, ok: bool, detail: str = "") -> None:
        mark = "✅" if ok else "❌"
        if not ok:
            self.failed += 1
        self.lines.append(f"- {mark} {title}")
        if detail:
            self.lines.append("")
            self.lines.append("  ```")
            self.lines.extend("  " + l for l in detail.rstrip().splitlines()[-40:])
            self.lines.append("  ```")
            self.lines.append("")

    def text(self) -> str:
        head = "**All checks passed.**" if not self.failed else f"**{self.failed} check(s) failed.**"
        return "\n".join(self.lines[:2] + [head, ""] + self.lines[2:]) + "\n"


def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=600)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"{' '.join(cmd)}\n{exc}"
    return proc.returncode == 0, f"$ {' '.join(cmd)}\n{proc.stdout}{proc.stderr}\nexit: {proc.returncode}"


def semver_core(version: str) -> tuple[int, ...] | None:
    core = version.split("+", 1)[0].split("-", 1)[0]
    if not re.fullmatch(r"\d+\.\d+\.\d+", core):
        return None
    return tuple(int(x) for x in core.split("."))


def git_show(ref: str, path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    ok, out = run(["git", "show", f"{ref}:{rel}"])
    if not ok:
        return None
    return out.split("\n", 1)[1].rsplit("\nexit:", 1)[0]


def check_manifests(rep: Report, base_ref: str) -> None:
    a = json.loads(CLAUDE_MANIFEST.read_text(encoding="utf-8"))
    b = json.loads(CODEX_MANIFEST.read_text(encoding="utf-8"))
    same = a.get("name") == b.get("name") and a.get("description") == b.get("description") \
        and semver_core(a.get("version", "")) == semver_core(b.get("version", ""))
    rep.check("Claude and Codex plugin manifests agree on name, description, and version core",
              same, f"claude: {a.get('version')}\ncodex:  {b.get('version')}")
    core = semver_core(a.get("version", ""))
    rep.check("Claude manifest version is plain semver", core is not None and "+" not in a.get("version", ""),
              a.get("version", ""))
    base_text = git_show(base_ref, CLAUDE_MANIFEST)
    if base_text is None:
        rep.lines.append(f"- ⚪ Version bump vs {base_ref}: skipped (ref unavailable)")
        return
    base = semver_core(json.loads(base_text).get("version", ""))
    rep.check(f"Plugin version bumped above {base_ref} ({'.'.join(map(str, base)) if base else '?'})",
              core is not None and base is not None and core > base)


def check_readme(rep: Report, skill: str) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rep.check(f"README catalog lists **{skill}**", f"**{skill}**" in readme)
    dirs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    m = re.search(r"with (\w+) skills", readme)
    stated = None
    if m:
        stated = NUMBER_WORDS.get(m.group(1).lower(), int(m.group(1)) if m.group(1).isdigit() else None)
    rep.check(f"README skill count matches {len(dirs)} skill directories",
              stated == len(dirs), f"README says: {m.group(1) if m else 'not found'}")


def check_removed(rep: Report, skill: str) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rep.check(f"{skill}/ folder is removed", not (SKILLS / skill).exists())
    rep.check(f"README no longer mentions {skill}", skill not in readme)
    dirs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    m = re.search(r"with (\w+) skills", readme)
    stated = None
    if m:
        stated = NUMBER_WORDS.get(m.group(1).lower(), int(m.group(1)) if m.group(1).isdigit() else None)
    rep.check(f"README skill count matches {len(dirs)} skill directories",
              stated == len(dirs), f"README says: {m.group(1) if m else 'not found'}")


def check_skill_package(rep: Report, skill: str) -> None:
    d = SKILLS / skill
    rep.check(f"{skill}/SKILL.md exists", (d / "SKILL.md").exists())
    if not (d / "SKILL.md").exists():
        return
    text = (d / "SKILL.md").read_text(encoding="utf-8")
    broken = [t for t in LINK.findall(text) if not (d / t).resolve().is_relative_to(d.resolve()) or not (d / t).exists()]
    rep.check("Relative links in SKILL.md resolve inside the skill folder", not broken, "\n".join(broken))
    y = d / "agents" / "openai.yaml"
    rep.check(f"{skill}/agents/openai.yaml exists", y.exists())
    if y.exists():
        ytext = y.read_text(encoding="utf-8")
        short = re.search(r'short_description:\s*"?([^"\n]*)"?', ytext)
        length = len(short.group(1).strip()) if short else 0
        rep.check("openai.yaml short_description is 25–64 characters", 25 <= length <= 64, f"{length} chars")
        rep.check(f"openai.yaml default_prompt mentions ${skill}", f"${skill}" in ytext)
    stray = [p.relative_to(d).as_posix() for p in d.rglob("*")
             if p.is_file() and (p.name.lower().startswith(("readme", "changelog")) or p.suffix in {".sh", ".exe", ".zip"} or "/node_modules/" in p.as_posix())]
    rep.check("No README/changelog/executables/vendored files inside the skill", not stray, "\n".join(stray))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--removed", action="store_true", help="the change deletes this skill")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    rep = Report()
    for script in TEST_COMMANDS:
        ok, out = run([sys.executable, script])
        rep.check(f"`{script}`", ok, "" if ok else out)

    claude = shutil.which("claude")
    if claude:
        # The validator takes a plugin dir, a marketplace root, or a components dir (all skills), never one skill.
        for target in ("plugins/marq-sales-suite", "plugins/marq-sales-suite/skills", ".claude/skills", "."):
            ok, out = run([claude, "plugin", "validate", "--strict", target])
            rep.check(f"`claude plugin validate --strict {target}`", ok, "" if ok else out)
    else:
        rep.lines.append("- ⚪ `claude plugin validate`: skipped (CLI not installed on this runner)")

    check_manifests(rep, args.base_ref)
    if args.removed:
        check_removed(rep, args.skill)
    else:
        check_readme(rep, args.skill)
        check_skill_package(rep, args.skill)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(rep.text(), encoding="utf-8")
    print(rep.text())
    return 0 if rep.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
