import copy
import unittest

from campusflow.errors import TransitionError, ValidationError
from campusflow.notes import add_note, get_notes, next_note_id


class TestNotes(unittest.TestCase):
    def test_valid_note_and_correct_id(self):
        tickets = [{
            "id": "T001",
            "title": "Wi-Fi outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": "Ada",
            "notes": [],
        }]

        note = add_note(tickets, "T001", " Ada ", "   Initial triage started.   ")

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Ada")
        self.assertEqual(note["message"], "Initial triage started.")
        self.assertEqual(len(get_notes(tickets, "T001")), 1)

    def test_blank_or_short_note_rejected_without_consuming_id(self):
        tickets = [{
            "id": "T001",
            "title": "Wi-Fi outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": "Ada",
            "notes": [],
        }]
        before = copy.deepcopy(tickets)
        with self.assertRaises((ValidationError, TransitionError)):
            add_note(tickets, "T001", "Ada", "   ")
        self.assertEqual(tickets, before)

        with self.assertRaises((ValidationError, TransitionError)):
            add_note(tickets, "T001", "Ada", "Test")
        self.assertEqual(tickets, before)
        self.assertEqual(next_note_id(tickets[0]), "N001")

    def test_resolved_note_rejected_then_accepted_after_reopen(self):
        tickets = [{
            "id": "T001",
            "title": "Wi-Fi outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "resolved",
            "assigned_to": "Ada",
            "notes": [],
        }]
        with self.assertRaises(TransitionError):
            add_note(tickets, "T001", "Ada", "Needs follow-up")

        tickets[0]["status"] = "open"
        note = add_note(tickets, "T001", "Ada", "Needs follow-up")
        self.assertEqual(note["note_id"], "N001")

    def test_note_length_boundaries(self):
        tickets = [{
            "id": "T001",
            "title": "Wi-Fi outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": "Ada",
            "notes": [],
        }]
        note_ok_5 = "12345"
        note_ok_300 = "x" * 300
        note_bad_4 = "1234"
        note_bad_301 = "x" * 301

        add_note(tickets, "T001", "Ada", note_ok_5)
        self.assertEqual(len(tickets[0]["notes"]), 1)
        add_note(tickets, "T001", "Ada", note_ok_300)
        self.assertEqual(len(tickets[0]["notes"]), 2)

        with self.assertRaises(ValidationError):
            add_note(tickets, "T001", "Ada", note_bad_4)
        with self.assertRaises(ValidationError):
            add_note(tickets, "T001", "Ada", note_bad_301)


if __name__ == "__main__":
    unittest.main()
