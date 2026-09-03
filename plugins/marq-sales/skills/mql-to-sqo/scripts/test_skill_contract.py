from pathlib import Path
import unittest


SKILL_TEXT = Path(__file__).parents[1].joinpath("SKILL.md").read_text(encoding="utf-8")


class DealResolutionContractTest(unittest.TestCase):
    def test_deal_name_can_resolve_without_a_hubspot_url(self) -> None:
        self.assertIn("deal name, or company name", SKILL_TEXT)
        self.assertIn(
            "search the authenticated rep's accessible HubSpot deals by deal name",
            SKILL_TEXT,
        )
        self.assertIn("search HubSpot companies by company name", SKILL_TEXT)
        self.assertIn("retrieve its associated deals", SKILL_TEXT)
        self.assertIn("one clear match", SKILL_TEXT)
        self.assertIn("ask the user to confirm it", SKILL_TEXT)
        self.assertIn("multiple plausible matches", SKILL_TEXT)
        self.assertIn("ask the user to choose", SKILL_TEXT)
        self.assertIn("If there is no plausible match", SKILL_TEXT)
        self.assertIn("treat the result as ambiguous", SKILL_TEXT)
        self.assertNotIn(
            "Require the HubSpot deal-record link before beginning", SKILL_TEXT
        )


if __name__ == "__main__":
    unittest.main()
