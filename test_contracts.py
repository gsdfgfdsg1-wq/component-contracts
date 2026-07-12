import unittest
from contracts import compare


class ContractTests(unittest.TestCase):
    def test_removed_prop_is_major(self):
        before = {"Button": {"props": {"tone": {"values": ["primary"]}}}}
        report = compare(before, {"Button": {"props": {}}})
        self.assertEqual(report["recommended_bump"], "major")
        self.assertEqual(report["changes"][0]["kind"], "prop-removed")

    def test_default_change_is_minor(self):
        before = {"Alert": {"props": {"open": {"default": True}}}}
        after = {"Alert": {"props": {"open": {"default": False}}}}
        self.assertEqual(compare(before, after)["recommended_bump"], "minor")

    def test_added_optional_prop_is_patch(self):
        before = {"Card": {"props": {}}}
        after = {"Card": {"props": {"shadow": {"required": False}}}}
        self.assertEqual(compare(before, after)["recommended_bump"], "patch")


if __name__ == "__main__":
    unittest.main()
