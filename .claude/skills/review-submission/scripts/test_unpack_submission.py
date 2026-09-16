#!/usr/bin/env python3
"""Tests for unpack_submission.py. Run: python3 test_unpack_submission.py"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import unpack_submission as u  # noqa: E402

GOOD = """---
kind: skill-proposal
skill_name: demo-skill
submitted_by: Test Rep
summary: A demo
---
This skill does a demo thing.

--- file: SKILL.md ---
---
name: demo-skill
description: Demo skill for tests. Use when testing the unpacker.
---

# Demo

Read [the notes](references/notes.md).

--- file: agents/openai.yaml ---
interface:
  display_name: "Demo Skill"
  short_description: "Demo skill used by the unpacker tests"
  default_prompt: "Use $demo-skill to demo."

--- file: references/notes.md ---
```markdown
Notes body.
```
"""


class UnpackTests(unittest.TestCase):
    def test_happy_path(self):
        r = u.unpack(GOOD)
        self.assertTrue(r["ok"], r["errors"])
        self.assertEqual(r["skill_name"], "demo-skill")
        self.assertEqual([f["path"] for f in r["files"]], ["SKILL.md", "agents/openai.yaml", "references/notes.md"])
        self.assertEqual(r["description"], "This skill does a demo thing.")

    def test_fence_stripped(self):
        r = u.unpack(GOOD)
        notes = next(f for f in r["files"] if f["path"] == "references/notes.md")
        self.assertEqual(notes["content"], "Notes body.\n")

    def test_path_traversal_rejected(self):
        bad = GOOD + "\n--- file: ../../evil.md ---\nx\n"
        r = u.unpack(bad)
        self.assertFalse(r["ok"])
        self.assertTrue(any("unsafe path" in e for e in r["errors"]))

    def test_disallowed_kind_rejected(self):
        bad = GOOD + "\n--- file: scripts/run.sh ---\necho hi\n"
        r = u.unpack(bad)
        self.assertTrue(any("not allowed" in e for e in r["errors"]))

    def test_secret_detected(self):
        # Assembled at runtime so the literal never lands in the repo and trips push protection.
        fake = "xox" + "b-" + "1234567890-" + "abcdefghijklmnop"
        bad = GOOD.replace("Notes body.", "token " + fake)
        r = u.unpack(bad)
        self.assertTrue(any("Slack token" in e for e in r["errors"]))

    def test_name_mismatch(self):
        bad = GOOD.replace("\nname: demo-skill", "\nname: other-skill")
        r = u.unpack(bad)
        self.assertTrue(any("must equal skill_name" in e for e in r["errors"]))

    def test_missing_kind(self):
        r = u.unpack(GOOD.replace("kind: skill-proposal\n", ""))
        self.assertTrue(any("kind: skill-proposal" in e for e in r["errors"]))

    def test_collision_is_case_and_punctuation_insensitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "Demo_Skill").mkdir()
            r = u.unpack(GOOD, Path(tmp))
            self.assertEqual(r["collision"], "Demo_Skill")
            self.assertFalse(r["ok"])

    def test_install_only_when_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            install = Path(tmp) / "skills"
            install.mkdir()
            bundle = Path(tmp) / "b.md"
            bundle.write_text(GOOD, encoding="utf-8")
            rc = u.main([str(bundle), "--out", str(out), "--install-to", str(install), "--report", str(Path(tmp) / "r.json")])
            self.assertEqual(rc, 0)
            self.assertTrue((install / "demo-skill" / "SKILL.md").exists())
            bundle.write_text(GOOD.replace("\nname: demo-skill", "\nname: nope"), encoding="utf-8")
            rc = u.main([str(bundle), "--out", str(Path(tmp) / "out2"), "--install-to", str(Path(tmp) / "skills2")])
            self.assertEqual(rc, 2)
            self.assertFalse((Path(tmp) / "skills2").exists())

    def test_block_scalar_description(self):
        text = GOOD.replace(
            "description: Demo skill for tests. Use when testing the unpacker.",
            "description: >\n  Folded line one\n  folded line two.",
        )
        r = u.unpack(text)
        self.assertTrue(r["ok"], r["errors"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
