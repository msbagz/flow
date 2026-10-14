import json
import os
import tempfile
from pathlib import Path

from campusflow.errors import StorageError
from campusflow.validation import validate_ticket, ticket_id_number

FILENAME = Path("tickets.json")


def _resolve_path(path):
    if path is None:
        return FILENAME
    return Path(path)


def load_tickets(path=None) -> list[dict]:
    target = _resolve_path(path)
    if not target.exists():
        return []

    try:
        with target.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        raise StorageError(f"Invalid JSON in {target}: {error}") from error

    if not isinstance(raw_data, list):
        raise StorageError(f"{target} must contain a list of tickets")

    normalized = []
    seen_ids = set()
    for item in raw_data:
        if not isinstance(item, dict):
            raise StorageError("Each ticket must be a dictionary")
        candidate = dict(item)
        candidate.setdefault("notes", [])
        validated = validate_ticket(candidate)
        ticket_id = validated["id"]
        if ticket_id in seen_ids:
            raise StorageError(f"Duplicate ticket ID '{ticket_id}' in {target}")
        seen_ids.add(ticket_id)
        seen_note_ids = set()
        for note in validated["notes"]:
            note_id = note["note_id"]
            if note_id in seen_note_ids:
                raise StorageError(f"Duplicate note ID '{note_id}' in ticket '{ticket_id}'")
            seen_note_ids.add(note_id)
        normalized.append(validated)

    return normalized


def save_tickets(path=None, tickets=None) -> None:
    if tickets is None and isinstance(path, (list, tuple)):
        tickets = list(path)
        path = FILENAME
    elif tickets is None:
        tickets = []
    target = _resolve_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    validated = []
    for ticket in tickets:
        validated.append(validate_ticket(ticket))

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            delete=False,
            dir=str(target.parent),
            encoding="utf-8",
        ) as file:
            json.dump(validated, file, indent=4)
            temp_path = file.name
        os.replace(temp_path, target)
    except OSError as error:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise StorageError(f"Could not save tickets to {target}: {error}") from error


def next_ticket_id(tickets):
    if not tickets:
        return "T001"
    highest = 0
    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue
        ticket_id = ticket.get("id")
        if isinstance(ticket_id, str):
            try:
                highest = max(highest, ticket_id_number(ticket_id))
            except ValueError:
                continue
    return f"T{highest + 1:03d}"
