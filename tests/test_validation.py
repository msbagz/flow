import copy
import unittest

from campusflow.errors import TransitionError, ValidationError
from campusflow.validation import (
    calculate_priority,
    can_transition,
    validate_affected_users,
    validate_ticket,
)


class TestPriorityAndValidation(unittest.TestCase):
    def test_priority_precedence(self):
        self.assertEqual(calculate_priority("high", 12), "critical")
        self.assertEqual(calculate_priority("high", 2), "high")
        self.assertEqual(calculate_priority("low", 10), "high")
        self.assertEqual(calculate_priority("low", 4), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_invalid_affected_users_are_rejected(self):
        for value in (0, -1, 1.5, "3", True):
            with self.assertRaises(ValidationError):
                validate_affected_users(value)

    def test_open_unassigned_ticket_cannot_move_to_in_progress(self):
        ticket = {
            "id": "T001",
            "title": "Wi-Fi outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": [],
        }
        state = copy.deepcopy(ticket)
        with self.assertRaises(TransitionError):
            can_transition(ticket, "in_progress")
        self.assertEqual(ticket, state)

    def test_validate_ticket_rejects_priority_mismatch(self):
        ticket = {
            "id": "T002",
            "title": "Hardware failure",
            "category": "Hardware",
            "urgency": "high",
            "affected_users": 2,
            "priority": "low",
            "status": "open",
            "assigned_to": None,
            "notes": [],
        }
        with self.assertRaises(ValidationError):
            validate_ticket(ticket)


if __name__ == "__main__":
    unittest.main()
