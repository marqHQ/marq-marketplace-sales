#!/usr/bin/env python3
"""Regression checks for MAP readiness, provenance, and stale installations."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import validate_map

ROOT = Path(__file__).resolve().parent.parent


def fixture() -> dict:
    prompt = (ROOT / "references/transcript-analysis-prompt.md").read_text()
    payload = json.loads(prompt.split("```json\n", 1)[1].split("```", 1)[0])
    payload["evidence_coverage"].update(
        status="ready", availability_status="transcript_ready",
        confirmed_challenges=3, sources_reviewed=["test-source"],
    )
    payload["evidence_sources"] = [{
        "source_id": "test-source", "title": "Synthetic regression transcript",
        "date": "2026-10-12", "source_url": None, "meeting_host": "customer",
        "transcript_source": "pasted", "participants": ["Synthetic Customer"],
        "full_transcript": "Synthetic Customer: Our team manually updates every document for each local office every week.",
        "selection_reason": "Synthetic validator fixture", "evidence_role": "discovery",
    }]
    for i in range(1, 4):
        payload["marq_fields"].update({
            f"challenge {i} title": "Manual Updates",
            f"challenge {i} summary": "Local teams manually update documents every week and central marketing reviews each version before release.",
            f"challenge {i} quote": "Our team manually updates every document for each local office every week.",
            f"solution {i} title": "Controlled Templates",
            f"solution {i} summary": "Approved templates let local teams update permitted details while central marketing maintains document brand standards.",
            f"solution {i} outcome": "Reduce repeated document preparation while keeping approved brand standards intact.",
        })
        payload["quote_evidence"][f"challenge {i} quote"].update(
            source_id="test-source", source_title="Synthetic regression transcript",
            source_date="2026-10-12", source_url=None, meeting_host="customer",
            transcript_source="pasted", speaker="Synthetic Customer", timestamp=None,
            transcript_excerpt="Our team manually updates every document for each local office every week.",
            presentation_edits=[], reported_speech=False,
        )
    payload["review"]["status"] = "PASS_READY"
    # Repeated content deliberately shows that these mechanical checks do not
    # replace an independent review of distinctness or factual attribution.
    return payload


class MapValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="map-validator-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "analysis.json"
        self.payload = fixture()

    def validate(self, payload: object | None = None) -> list[str]:
        self.path.write_text(json.dumps(self.payload if payload is None else payload))
        return validate_map.validate(self.path)

    def rejects(self, message: str) -> None:
        self.assertTrue(any(message in error for error in self.validate()), message)

    def test_ready_structural_fixture(self) -> None:
        self.assertEqual([], self.validate())

    def test_pending_schema_fixture(self) -> None:
        prompt = (ROOT / "references/transcript-analysis-prompt.md").read_text()
        pending = json.loads(prompt.split("```json\n", 1)[1].split("```", 1)[0])
        self.assertEqual([], self.validate(pending))

    def test_ready_requires_three(self) -> None:
        self.payload["evidence_coverage"]["confirmed_challenges"] = 2
        self.rejects("exactly 3")

    def test_ready_requires_usable_transcript_status(self) -> None:
        self.payload["evidence_coverage"]["availability_status"] = "transcript_insufficient"
        self.rejects("transcript_ready availability")

    def test_ready_requires_reviewed_sources(self) -> None:
        self.payload["evidence_coverage"]["sources_reviewed"] = []
        self.rejects("at least one reviewed source")

    def test_reviewed_sources_are_ids(self) -> None:
        self.payload["evidence_coverage"]["sources_reviewed"] = [{"source_id": "test-source"}]
        self.rejects("source ID strings only")

    def test_unknown_reviewed_source(self) -> None:
        self.payload["evidence_coverage"]["sources_reviewed"] = ["absent-source"]
        self.rejects("unknown source IDs")

    def test_ready_requires_evidence(self) -> None:
        self.payload["evidence_sources"] = []
        self.rejects("at least one usable evidence source")

    def test_blank_and_null_transcripts(self) -> None:
        for value in ("", "  ", None):
            with self.subTest(value=value):
                self.payload["evidence_sources"][0]["full_transcript"] = value
                self.rejects("full_transcript must be a non-empty string")

    def test_empty_participants(self) -> None:
        self.payload["evidence_sources"][0]["participants"] = []
        self.rejects("participants must be a non-empty array")

    def test_duplicate_source_id(self) -> None:
        self.payload["evidence_sources"].append(copy.deepcopy(self.payload["evidence_sources"][0]))
        self.rejects("source_id is duplicated")

    def test_empty_quote_provenance(self) -> None:
        for key in ("speaker", "transcript_excerpt"):
            with self.subTest(key=key):
                self.payload = fixture()
                self.payload["quote_evidence"]["challenge 1 quote"][key] = ""
                self.rejects(f"{key} must be a non-empty string")

    def test_quote_must_exist_in_its_source(self) -> None:
        self.payload["quote_evidence"]["challenge 1 quote"]["transcript_excerpt"] = "This quotation was not in the transcript."
        self.rejects("not contiguous in its source transcript")

    def test_quote_source_must_be_reviewed(self) -> None:
        source = copy.deepcopy(self.payload["evidence_sources"][0])
        source["source_id"] = "unreviewed"
        self.payload["evidence_sources"].append(source)
        self.payload["quote_evidence"]["challenge 1 quote"]["source_id"] = "unreviewed"
        self.rejects("not in sources_reviewed")

    def test_copy_limits(self) -> None:
        self.payload["marq_fields"]["challenge 1 title"] = "An Overly Long Challenge Title"
        self.rejects("maximum is 3")

    def test_whitespace_only_title(self) -> None:
        self.payload["marq_fields"]["challenge 1 title"] = "   "
        self.rejects("challenge 1 title is required")

    def test_pending_review_before_independent_review(self) -> None:
        self.payload["review"]["status"] = "pending"
        self.assertEqual([], self.validate())

    def test_review_and_coverage_must_agree(self) -> None:
        self.payload["review"]["status"] = "PASS_INSUFFICIENT"
        self.rejects("PASS_INSUFFICIENT requires insufficient_evidence")

    def test_cli_exit_status(self) -> None:
        self.validate()
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_map.py"), str(self.path)], capture_output=True)
        self.assertEqual(0, result.returncode)
        self.path.write_text("not JSON")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_map.py"), str(self.path)], capture_output=True)
        self.assertEqual(1, result.returncode)


class TemplateMapTests(unittest.TestCase):
    def check_map(self, value: object) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory(prefix="template-validator-") as temp:
            path = Path(temp) / "templates.json"
            path.write_text(json.dumps(value))
            return subprocess.run([sys.executable, str(ROOT / "scripts/validate_template_map.py"), str(path)], capture_output=True, text=True)

    def test_canonical_map(self) -> None:
        result = self.check_map(json.loads((ROOT / "references/template-map.json").read_text()))
        self.assertEqual(0, result.returncode, result.stderr)

    def test_each_missing_or_invalid_industry(self) -> None:
        original = json.loads((ROOT / "references/template-map.json").read_text())
        for key in original:
            for value in (None, "", "not-a-uuid", " " + original[key], original[key] + " "):
                with self.subTest(key=key, value=value):
                    changed = dict(original)
                    changed[key] = value
                    result = self.check_map(changed)
                    self.assertEqual(1, result.returncode)
                    self.assertIn(key, result.stderr)
                    self.assertIn("STALE_TEMPLATE_MAP", result.stderr)

    def test_malformed_root(self) -> None:
        for root in ([], None, "bad map"):
            with self.subTest(root=root):
                result = self.check_map(root)
                self.assertEqual(1, result.returncode)
                self.assertIn("STALE_TEMPLATE_MAP", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
