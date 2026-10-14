
import unittest
from unittest.mock import patch

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    list_tickets,
    validate_affected_users,
    validate_category,
    validate_title,
    validate_urgency,
    view_ticket,
)


class TestTicketValidation(unittest.TestCase):
    @patch("builtins.input", side_effect=["", "  Internet is down  "])
    @patch("builtins.print")
    def test_validate_title_retries_empty_input(
        self, mock_print, mock_input
    ):
        result = validate_title()

        self.assertEqual(result, "Internet is down")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["invalid", "network"])
    @patch("builtins.print")
    def test_validate_category_retries_invalid_input(
        self, mock_print, mock_input
    ):
        result = validate_category()

        self.assertEqual(result, "Network")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["urgent", "HIGH"])
    @patch("builtins.print")
    def test_validate_urgency_normalizes_case(
        self, mock_print, mock_input
    ):
        result = validate_urgency()

        self.assertEqual(result, "high")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["0", "-2", "abc", "5"])
    @patch("builtins.print")
    def test_validate_affected_users_requires_positive_integer(
        self, mock_print, mock_input
    ):
        result = validate_affected_users()

        self.assertEqual(result, 5)
        self.assertEqual(mock_input.call_count, 4)


class TestPriorityCalculation(unittest.TestCase):
    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_with_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_medium_urgency_is_at_least_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_low_urgency_with_many_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_urgency_with_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")


class TestTicketOperations(unittest.TestCase):
    @patch(
        "campusflow.tickets.validate_title",
        return_value="Internet is down",
    )
    @patch("campusflow.tickets.validate_category", return_value="Network")
    @patch("campusflow.tickets.validate_urgency", return_value="high")
    @patch("campusflow.tickets.validate_affected_users", return_value=12)
    def test_create_ticket_adds_ticket_to_list(
        self, mock_users, mock_urgency, mock_category, mock_title
    ):
        tickets = []

        ticket = create_ticket(tickets)

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Internet is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(tickets), 1)
        self.assertIs(tickets[0], ticket)

    @patch(
        "campusflow.tickets.validate_title",
        return_value="Broken keyboard",
    )
    @patch("campusflow.tickets.validate_category", return_value="Hardware")
    @patch("campusflow.tickets.validate_urgency", return_value="low")
    @patch("campusflow.tickets.validate_affected_users", return_value=1)
    def test_create_ticket_generates_next_id(
        self, mock_users, mock_urgency, mock_category, mock_title
    ):
        tickets = [{"id": "T007"}]

        ticket = create_ticket(tickets)

        self.assertEqual(ticket["id"], "T008")

    
@patch("builtins.print")
def test_list_tickets_displays_ticket(self, mock_print):
    tickets = [
        {
            "id": "T001",
            "title": "Internet is down",
            "priority": "critical",
            "status": "open",
        }
    ]

    list_tickets(tickets)

    output = " ".join(
        str(call.args[0]) if call.args else ""
        for call in mock_print.call_args_list
    )

    self.assertIn("T001", output)
    self.assertIn("Internet is down", output)

    @patch("builtins.print")
    def test_list_tickets_handles_empty_list(self, mock_print):
        list_tickets([])

        mock_print.assert_called_once_with("No tickets found.")

    @patch("builtins.input", return_value="t001")
    @patch("builtins.print")
    def test_view_ticket_finds_id_case_insensitively(
        self, mock_print, mock_input
    ):
        tickets = [{"id": "T001", "title": "Internet is down"}]

        view_ticket(tickets)

        output = " ".join(
            str(call.args[0]) for call in mock_print.call_args_list
        )
        self.assertIn("Internet is down", output)

    @patch("builtins.input", return_value="T999")
    @patch("builtins.print")
    def test_view_ticket_reports_missing_ticket(
        self, mock_print, mock_input
    ):
        view_ticket([])

        mock_print.assert_called_once_with("Ticket not found.")


if __name__ == "__main__":
    unittest.main()