import copy
import unittest

from update import refresh_status


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.before = {"park": {"last_checked_at": "2026-10-01T00:00:00Z"},
                       "oh": {"last_checked_at": "2026-10-02T00:00:00Z"}}
        self.now = "2026-10-08T01:00:00Z"

    def test_empty_successful_check_advances_without_touching_other_people(self):
        original = copy.deepcopy(self.before)
        result = refresh_status(self.before, [{"researcher_id": "oh", "status": "ok", "records": 0}],
                                self.now, ["park", "oh"])
        self.assertEqual(result["oh"]["last_checked_at"], self.now)
        self.assertEqual(result["park"], self.before["park"])
        self.assertEqual(self.before, original)

    def test_shared_success_does_not_mask_failed_personal_checks(self):
        rows = [{"researcher_id": "oh", "status": "failed"},
                {"researcher_id": "shared", "status": "ok"}]
        result = refresh_status(self.before, rows, self.now, ["park", "oh"])
        self.assertEqual(result["oh"]["last_checked_at"], self.before["oh"]["last_checked_at"])
        self.assertEqual(result["oh"]["status"], "failed")
        self.assertEqual(result["oh"]["last_attempt_at"], self.now)
        self.assertEqual(result["park"], self.before["park"])

    def test_partial_failures_are_disclosed(self):
        rows = [{"researcher_id": "oh", "status": "partial"},
                {"researcher_id": "oh", "status": "failed"}]
        result = refresh_status(self.before, rows, self.now, ["oh"])
        self.assertEqual(result["oh"]["last_checked_at"], self.now)
        self.assertEqual(result["oh"]["status"], "partial")
        self.assertEqual(result["oh"]["failed_sources"], 1)

    def test_shared_only_check_preserves_personal_timestamps(self):
        self.assertEqual(refresh_status(self.before, [{"researcher_id": "shared", "status": "ok"}],
                                        self.now, ["park", "oh"]), self.before)


if __name__ == "__main__":
    unittest.main()
