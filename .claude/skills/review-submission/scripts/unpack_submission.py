#!/usr/bin/env python3
"""Unpack a skill-proposal bundle into a skill directory with deterministic checks.

The rep-facing `upload-new-skill` skill emits one text bundle per proposal:

    ---
    kind: skill-proposal
    skill_name: my-skill
    submitted_by: Jane Rep
    summary: One line
    ---
    Free-form description (markdown).

    --- file: SKILL.md ---
    <content>
    --- file: agents/openai.yaml ---
    <content>

Everything a model should never be trusted to judge lives here instead: path
safety, allowed file types, size caps, secret scan, name rules, and collisions
with existing skills. Exit codes: 0 ok, 2 blocking errors, 1 usage/parse failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

FILE_MARK = re.compile(r"^--- file: (?P<path>\S.*?) ---\s*$")
FENCE_OPEN = re.compile(r"^```[\w+.-]*\s*$")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BLOCK_SCALARS = {">", "|", ">-", "|-", ">+", "|+"}

MAX_FILES = 40
MAX_FILE_BYTES = 200_000
MAX_TOTAL_BYTES = 1_000_000
MAX_DESCRIPTION_BYTES = 800  # ChatGPT/Codex plugin manifest tolerance observed 2026-09

ALLOWED_PATHS = [
    (re.compile(r"^SKILL\.md$"), "skill"),
    (re.compile(r"^agents/openai\.yaml$"), "interface"),
    (re.compile(r"^references/[^/]+\.md$"), "reference"),
    (re.compile(r"^scripts/[^/]+\.py$"), "script"),
    (re.compile(r"^assets/[^/]+\.(?:md|txt|json|ya?ml|csv|html|svg)$"), "asset"),
]

SECRET_PATTERNS = [
    ("Slack token", re.compile(r"xox[abposr]-[A-Za-z0-9-]{10,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("GitHub fine-grained PAT", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI API key", re.compile(r"\bsk-(?!ant-)(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("HubSpot private-app token", re.compile(r"\bpat-(?:na|eu)\d-[0-9a-f-]{30,}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{30,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
]
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FIXME|lorem ipsum)\b|<[^>\n]*placeholder[^>\n]*>", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL = re.compile(r"https?://[^\s)>\]]+")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (meta, body) from a leading `---` block. Stdlib-only, flat keys.

    Handles `key: value`, quoted values, and YAML block scalars (`>` / `|`)
    well enough for skill frontmatter. Nested mappings are ignored.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text
    meta: dict[str, str] = {}
    i = 1
    while i < end:
        line = lines[i]
        if ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            value = value.strip()
            if value in BLOCK_SCALARS:
                block = []
                i += 1
                while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                    block.append(lines[i].strip())
                    i += 1
                joiner = "\n" if value.startswith("|") else " "
                meta[key.strip()] = joiner.join(b for b in block if b).strip()
                continue
            meta[key.strip()] = value.strip("'\"")
        i += 1
    return meta, "\n".join(lines[end + 1:])


def strip_fence(content: str) -> str:
    """Remove a single code fence wrapping the whole file, if present."""
    lines = content.strip("\n").splitlines()
    if len(lines) >= 2 and FENCE_OPEN.match(lines[0]) and lines[-1].strip() == "```":
        lines = lines[1:-1]
    body = "\n".join(lines).rstrip("\n")
    return body + "\n" if body else ""


def split_files(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (description, [(raw_path, content)]) in bundle order."""
    description: list[str] = []
    files: list[tuple[str, list[str]]] = []
    for line in body.splitlines():
        match = FILE_MARK.match(line)
        if match:
            files.append((match.group("path").strip(), []))
        elif files:
            files[-1][1].append(line)
        else:
            description.append(line)
    return "\n".join(description).strip(), [(p, strip_fence("\n".join(c))) for p, c in files]


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def check_path(raw: str) -> tuple[str, str]:
    """Return (clean_posix_path, kind) or raise ValueError."""
    if "\\" in raw or raw.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", raw):
        raise ValueError(f"absolute or non-POSIX path: {raw}")
    parts = PurePosixPath(raw).parts
    if not parts or any(p in ("..", ".", "") or p.startswith(".") for p in parts):
        raise ValueError(f"unsafe path: {raw}")
    clean = "/".join(parts)
    for pattern, kind in ALLOWED_PATHS:
        if pattern.match(clean):
            return clean, kind
    raise ValueError(f"path not allowed by the package contract: {raw}")


def scan_text(path: str, content: str, errors: list[str], warnings: list[str]) -> None:
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(content):
            errors.append(f"{path}: possible {label} detected; remove it and resubmit")
    if "\x00" in content:
        errors.append(f"{path}: binary content is not accepted")
    if PLACEHOLDER.search(content):
        warnings.append(f"{path}: unfinished placeholder text (TODO/TBD/FIXME/placeholder)")
    emails = sorted(set(EMAIL.findall(content)))
    if emails:
        warnings.append(f"{path}: email addresses present in a public repo: {', '.join(emails[:5])}")
    urls = sorted(set(URL.findall(content)))
    if urls:
        warnings.append(f"{path}: external links to review: {', '.join(urls[:8])}")


def find_collision(install_root: Path, name: str) -> str | None:
    if not install_root.is_dir():
        return None
    wanted = normalize_name(name)
    for existing in install_root.iterdir():
        if existing.is_dir() and normalize_name(existing.name) == wanted:
            return existing.name
    return None


def unpack(text: str, install_root: Path | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    meta, body = parse_frontmatter(text)
    if meta.get("kind") != "skill-proposal":
        errors.append("bundle frontmatter must declare `kind: skill-proposal`")
    name = meta.get("skill_name", "")
    if not NAME_RE.match(name):
        errors.append("skill_name must use lowercase letters, digits, and single hyphens")

    description, raw_files = split_files(body)
    files: list[dict] = []
    seen: set[str] = set()
    total = 0
    for raw_path, content in raw_files:
        try:
            clean, kind = check_path(raw_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if clean in seen:
            errors.append(f"duplicate file: {clean}")
            continue
        seen.add(clean)
        data = content.encode("utf-8")
        total += len(data)
        if len(data) > MAX_FILE_BYTES:
            errors.append(f"{clean}: exceeds {MAX_FILE_BYTES} bytes")
        if not data.strip():
            errors.append(f"{clean}: file is empty")
        scan_text(clean, content, errors, warnings)
        files.append({
            "path": clean,
            "kind": kind,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "content": content,
        })
    if not raw_files:
        errors.append("no `--- file: <path> ---` blocks found in the bundle")
    if len(files) > MAX_FILES:
        errors.append(f"too many files ({len(files)} > {MAX_FILES})")
    if total > MAX_TOTAL_BYTES:
        errors.append(f"bundle too large ({total} bytes > {MAX_TOTAL_BYTES})")

    skill_md = next((f for f in files if f["path"] == "SKILL.md"), None)
    if skill_md is None:
        errors.append("SKILL.md is required")
    else:
        fm, _ = parse_frontmatter(skill_md["content"])
        if fm.get("name") != name:
            errors.append(f"SKILL.md frontmatter name {fm.get('name')!r} must equal skill_name {name!r}")
        desc = fm.get("description", "")
        if not desc:
            errors.append("SKILL.md frontmatter needs a non-empty description")
        elif len(desc.encode("utf-8")) > MAX_DESCRIPTION_BYTES:
            warnings.append(
                f"SKILL.md description is {len(desc.encode('utf-8'))} bytes; "
                f"keep it under {MAX_DESCRIPTION_BYTES} for plugin-manifest limits"
            )
    if not any(f["path"] == "agents/openai.yaml" for f in files):
        warnings.append("agents/openai.yaml missing; the reviewer will add interface metadata")

    collision = find_collision(install_root, name) if install_root and name else None
    if collision:
        errors.append(
            f"skill name collides with existing skill `{collision}`; "
            "use plugin-feedback to propose changes to an existing skill"
        )

    return {
        "ok": not errors,
        "skill_name": name,
        "meta": meta,
        "description": description,
        "files": files,
        "errors": errors,
        "warnings": warnings,
        "collision": collision,
    }


def write_tree(result: dict, root: Path) -> Path:
    target = root / result["skill_name"]
    for f in result["files"]:
        dest = target / f["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f["content"], encoding="utf-8", newline="\n")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bundle", help="path to the submission bundle (markdown)")
    parser.add_argument("--out", required=True, help="directory to unpack into (always written)")
    parser.add_argument("--install-to", help="skills root; files are installed here only when all checks pass")
    parser.add_argument("--report", help="write the JSON report here (file contents omitted)")
    args = parser.parse_args(argv)

    try:
        text = Path(args.bundle).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read bundle: {exc}", file=sys.stderr)
        return 1

    install_root = Path(args.install_to) if args.install_to else None
    result = unpack(text, install_root)
    if result["skill_name"]:
        write_tree(result, Path(args.out))
        if result["ok"] and install_root is not None:
            result["installed_to"] = str(write_tree(result, install_root))

    report = {k: v for k, v in result.items() if k != "files"}
    report["files"] = [{k: v for k, v in f.items() if k != "content"} for f in result["files"]]
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"skill: {result['skill_name'] or '(none)'}  files: {len(result['files'])}  ok: {result['ok']}")
    for e in result["errors"]:
        print(f"ERROR   {e}")
    for w in result["warnings"]:
        print(f"WARNING {w}")
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
