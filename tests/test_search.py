import unittest

from campusflow.search import search_tickets


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi outage in library",
                "category": "Network",
                "status": "open",
                "priority": "critical",
                "notes": [],
            },
            {
                "id": "T002",
                "title": "Laptop battery issue",
                "category": "Hardware",
                "status": "open",
                "priority": "high",
                "notes": [],
            },
            {
                "id": "T003",
                "title": "VPN login failure",
                "category": "Network",
                "status": "resolved",
                "priority": "medium",
                "notes": [],
            },
        ]

    def test_title_search_ignores_case(self):
        self.tickets[0]["title"] = "Wireless WiFi outage in library"
        matches = search_tickets(self.tickets, title_query="wifi")
        self.assertEqual([ticket["id"] for ticket in matches], ["T001"])

    def test_combined_filters_use_and_logic(self):
        self.tickets[0]["title"] = "Wireless WiFi outage in library"
        matches = search_tickets(self.tickets, title_query="wifi", category="Network", status="open")
        self.assertEqual([ticket["id"] for ticket in matches], ["T001"])


if __name__ == "__main__":
    unittest.main()
