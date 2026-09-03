#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path

from audit_utils import append_history, reconcile, score_deal


ROOT = Path(__file__).resolve().parent.parent


class FixtureTests(unittest.TestCase):
    def test_scoring_fixtures(self) -> None:
        fixtures = json.loads((ROOT / "references" / "scoring-fixtures.json").read_text())
        for fixture in fixtures:
            with self.subTest(fixture=fixture["name"]):
                result = score_deal(fixture["input"])
                for key, value in fixture["expected"].items():
                    self.assertEqual(result[key], value)


class HelperTests(unittest.TestCase):
    def test_append_preserves_history(self) -> None:
        result = append_history("Old line", "08 / 13 / 2026 - NEXT STEP NEEDED - no date")
        self.assertTrue(result["changed"])
        self.assertEqual(result["value"], "Old line\n08 / 13 / 2026 - NEXT STEP NEEDED - no date")

    def test_append_suppresses_normalized_duplicate(self) -> None:
        line = "08 / 13 / 2026 - NEXT STEP NEEDED - no date"
        result = append_history(f"Old line\n  {line.upper()}  ", line)
        self.assertFalse(result["changed"])

    def test_reconcile_complete(self) -> None:
        self.assertTrue(reconcile(3, ["1", "2", "3"])["complete"])

    def test_reconcile_rejects_duplicate(self) -> None:
        result = reconcile(3, ["1", "2", "2"])
        self.assertFalse(result["complete"])
        self.assertEqual(result["duplicates"], 1)

    def test_invalid_enum_fails(self) -> None:
        with self.assertRaises(ValueError):
            score_deal({
                "audit_date": "2026-08-13", "stage_band": "unknown",
                "has_actionable_next_step": True, "evidence_status": "aligned",
                "task_status": "none"
            })

    def test_relative_date_fails(self) -> None:
        with self.assertRaises(ValueError):
            score_deal({
                "audit_date": "2026-08-13", "stage_band": "early",
                "next_step_date": "next Tuesday", "has_actionable_next_step": True,
                "evidence_status": "aligned", "task_status": "none"
            })

    def test_activity_threshold_boundaries(self) -> None:
        base = {
            "audit_date": "2026-08-15", "stage_band": "early",
            "next_step_date": "2026-09-01", "has_actionable_next_step": True,
            "weak_next_step": False, "close_date": "2026-10-01",
            "evidence_status": "aligned", "task_status": "future_matching"
        }
        at_threshold = score_deal({**base, "last_activity_at": "2026-08-01"})
        at_double = score_deal({**base, "last_activity_at": "2026-07-18"})
        beyond_double = score_deal({**base, "last_activity_at": "2026-07-17"})
        self.assertEqual(at_threshold["components"]["activity_recency"], 30)
        self.assertEqual(at_threshold["color"], "green")
        self.assertEqual(at_double["components"]["activity_recency"], 15)
        self.assertEqual(at_double["color"], "yellow")
        self.assertIn("severe_inactivity", beyond_double["overrides"])


if __name__ == "__main__":
    unittest.main()
