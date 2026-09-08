#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path

from momentum_utils import score_momentum


ROOT = Path(__file__).resolve().parent.parent


class MomentumFixtureTests(unittest.TestCase):
    def test_all_rules(self) -> None:
        document = json.loads((ROOT / "references" / "momentum-fixtures.json").read_text())
        base = document["base"]
        for fixture in document["cases"]:
            with self.subTest(fixture=fixture["name"]):
                result = score_momentum({**base, **fixture["changes"]})
                self.assertEqual(result["color"], fixture["color"])
                if "reason" in fixture:
                    self.assertIn(fixture["reason"], result["warnings"] + result["overrides"])

    def test_invalid_enum_fails(self) -> None:
        document = json.loads((ROOT / "references" / "momentum-fixtures.json").read_text())
        with self.assertRaises(ValueError):
            score_momentum({**document["base"], "stage_band": "unknown"})

    def test_negative_engagement_age_fails(self) -> None:
        document = json.loads((ROOT / "references" / "momentum-fixtures.json").read_text())
        with self.assertRaises(ValueError):
            score_momentum({**document["base"], "days_since_meaningful_engagement": -1})


if __name__ == "__main__":
    unittest.main()
