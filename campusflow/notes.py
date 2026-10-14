"""Ticket note helpers.

Contract: add_note validates the target ticket and appends a note only after all
input checks pass. It raises ValidationError for invalid author/message values,
TransitionError when the ticket is resolved, and NotFoundError when the ticket
is missing. On success it returns the new note dict and mutates the in-memory
list in place. Rejected calls leave ticket state unchanged.
"""

from __future__ import annotations

import copy

from campusflow.errors import NotFoundError, TransitionError, ValidationError
from campusflow.validation import validate_note_message, validate_staff_label


def ticket_id_number(ticket_id):
    if not isinstance(ticket_id, str):
        raise ValidationError("Ticket ID must be a string")
    digits = ticket_id.strip()[1:]
    if not digits.isdigit():
        raise ValidationError(f"Invalid ticket ID: {ticket_id!r}")
    return int(digits)


def note_id_number(note_id):
    if not isinstance(note_id, str):
        raise ValidationError("Note ID must be a string")
    digits = note_id.strip()[1:]
    if not digits.isdigit():
        raise ValidationError(f"Invalid note ID: {note_id!r}")
    return int(digits)


def next_note_id(ticket):
    if not isinstance(ticket, dict):
        raise ValidationError("Ticket must be a dictionary")
    notes = ticket.get("notes", []) or []
    if not isinstance(notes, list):
        raise ValidationError("Ticket notes must be a list")
    highest = 0
    for note in notes:
        if not isinstance(note, dict):
            continue
        note_id = note.get("note_id", "")
        if isinstance(note_id, str) and note_id.upper().startswith("N"):
            try:
                highest = max(highest, note_id_number(note_id))
            except ValidationError:
                continue
    return f"N{highest + 1:03d}"


def add_note(tickets, ticket_id, author, message):
    if tickets is None:
        raise ValidationError("Tickets list cannot be None")
    if not isinstance(tickets, list):
        raise ValidationError("Tickets must be a list")

    ticket = None
    for item in tickets:
        if isinstance(item, dict) and item.get("id") == ticket_id:
            ticket = item
            break
    if ticket is None:
        raise NotFoundError(f"Ticket '{ticket_id}' not found")

    normalized_author = validate_staff_label(author)
    normalized_message = validate_note_message(message)
    status = str(ticket.get("status", "")).strip().casefold()
    if status not in {"open", "in_progress"}:
        raise TransitionError("Notes can only be added to open or in_progress tickets")

    ticket_copy = copy.deepcopy(ticket)
    ticket_copy.setdefault("notes", [])
    note = {
        "note_id": next_note_id(ticket_copy),
        "author": normalized_author,
        "message": normalized_message,
    }
    ticket_copy["notes"].append(note)
    ticket["notes"] = ticket_copy["notes"]
    return note


def get_notes(tickets, ticket_id):
    if not isinstance(tickets, list):
        raise ValidationError("Tickets must be a list")
    for ticket in tickets:
        if isinstance(ticket, dict) and ticket.get("id") == ticket_id:
            notes = ticket.get("notes", []) or []
            return sorted(notes, key=lambda note: note_id_number(note.get("note_id", "N000")))
    raise NotFoundError(f"Ticket '{ticket_id}' not found")
