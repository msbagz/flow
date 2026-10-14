
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from campusflow.errors import StorageError
from campusflow.storage import load_tickets, next_ticket_id, save_tickets


class TestTicketStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = Path(self.temp_dir.name) / "tickets.json"
        self.patcher = patch("campusflow.storage.FILENAME", self.filename)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def make_ticket(self, ticket_id="T001", title="Internet is down", priority="critical"):
        return {
            "id": ticket_id,
            "title": title,
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": priority,
            "status": "open",
            "assigned_to": None,
            "notes": [{"note_id": "N001", "author": "Ada", "message": "Started triage."}],
        }

    def test_missing_file_returns_empty_list(self):
        self.assertFalse(self.filename.exists())
        self.assertEqual(load_tickets(), [])

    def test_save_tickets_creates_json_file(self):
        tickets = [self.make_ticket()]
        save_tickets(tickets)
        self.assertTrue(self.filename.exists())
        with self.filename.open(encoding="utf-8") as file:
            saved_data = json.load(file)
        self.assertEqual(saved_data, tickets)

    def test_load_tickets_reads_saved_data(self):
        tickets = [self.make_ticket()]
        save_tickets(tickets)
        result = load_tickets()
        self.assertEqual(result, tickets)

    def test_save_and_load_multiple_tickets(self):
        tickets = [
            self.make_ticket(),
            {
                **self.make_ticket("T002", "Broken keyboard", "low"),
                "urgency": "low",
                "affected_users": 2,
                "priority": "low",
            },
        ]
        save_tickets(tickets)
        result = load_tickets()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "T001")
        self.assertEqual(result[1]["id"], "T002")
        self.assertEqual(next_ticket_id(result), "T003")

    def test_malformed_json_raises_storage_error(self):
        self.filename.write_text('{"id": "T001", invalid json', encoding="utf-8")
        with self.assertRaises(StorageError):
            load_tickets()

    def test_malformed_json_is_not_overwritten_by_loading(self):
        original_content = '{"broken": json'
        self.filename.write_text(original_content, encoding="utf-8")
        with self.assertRaises(StorageError):
            load_tickets()
        self.assertEqual(self.filename.read_text(encoding="utf-8"), original_content)

    def test_non_list_json_is_rejected(self):
        self.filename.write_text(json.dumps({"id": "T001"}), encoding="utf-8")
        with self.assertRaises(StorageError):
            load_tickets()

    def test_empty_list_is_saved_and_loaded(self):
        save_tickets([])
        self.assertEqual(load_tickets(), [])

    def test_duplicate_tickets_are_rejected_without_state_loss(self):
        tickets = [
            self.make_ticket("T001"),
            {**self.make_ticket("T001", "Duplicate", "high"), "urgency": "medium", "affected_users": 2, "priority": "medium"},
        ]
        save_tickets(self.filename, tickets)
        before = self.filename.read_text(encoding="utf-8")
        with self.assertRaises(StorageError):
            load_tickets(self.filename)
        self.assertEqual(self.filename.read_text(encoding="utf-8"), before)

    def test_legacy_ticket_without_notes_loads_with_empty_notes(self):
        legacy = [{
            "id": "T010",
            "title": "Old record",
            "category": "Other",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "open",
            "assigned_to": None,
        }]
        self.filename.write_text(json.dumps(legacy), encoding="utf-8")
        loaded = load_tickets(self.filename)
        self.assertEqual(loaded[0]["notes"], [])


if __name__ == "__main__":
    unittest.main()