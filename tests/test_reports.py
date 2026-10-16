import unittest

from campusflow.reports import format_report


class TestFormatReport(unittest.TestCase):
    def test_report_includes_a_clear_heading(self):
        report = {
            "total": 3,
            "by_status": {"open": 2, "in_progress": 1, "resolved": 0},
            "by_priority": {"critical": 1, "high": 1, "medium": 1, "low": 0},
            "unresolved": 3,
            "resolved": 0,
            "resolution_percent": 0.0,
        }

        output = format_report(report)

        self.assertIn("Ticket Report", output)
        self.assertIn("Status breakdown:", output)
        self.assertIn("Priority breakdown:", output)


if __name__ == "__main__":
    unittest.main()
