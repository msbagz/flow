import copy
import re

from campusflow.errors import TransitionError, ValidationError

CATEGORY_MAP = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}
VALID_CATEGORIES = tuple(CATEGORY_MAP.values())
VALID_URGENCIES = ("low", "medium", "high")
VALID_STATUSES = ("open", "in_progress", "resolved")
VALID_PRIORITIES = ("critical", "high", "medium", "low")


def ticket_id_number(ticket_id):
    if not isinstance(ticket_id, str):
        raise ValidationError("Ticket ID must be a string")
    cleaned = ticket_id.strip().upper()
    if not re.fullmatch(r"T\d+", cleaned):
        raise ValidationError(f"Invalid ticket ID: {ticket_id!r}")
    return int(cleaned[1:])


def calculate_priority(urgency: str, affected_users: int) -> str:
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def validate_category(value):
    if not isinstance(value, str):
        raise ValidationError("Category must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValidationError("Category cannot be blank")
    canonical = CATEGORY_MAP.get(normalized.casefold())
    if canonical is None:
        raise ValidationError(
            "Category must be one of: Network, Hardware, Software, Other"
        )
    return canonical


def validate_urgency(value):
    if not isinstance(value, str):
        raise ValidationError("Urgency must be a string")
    normalized = value.strip().casefold()
    if normalized not in VALID_URGENCIES:
        raise ValidationError("Urgency must be low, medium, or high")
    return normalized


def validate_title(value):
    if not isinstance(value, str):
        raise ValidationError("Title must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError("Title cannot be blank")
    return cleaned


def validate_affected_users(value):
    if isinstance(value, bool) or type(value) is not int:
        raise ValidationError("Affected users must be a positive integer")
    if value <= 0:
        raise ValidationError("Affected users must be a positive integer")
    return value


def validate_staff_label(value):
    if not isinstance(value, str):
        raise ValidationError("Staff label must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError("Staff label cannot be blank")
    return cleaned


def validate_ticket_id(value, existing_ids):
    if not isinstance(value, str):
        raise ValidationError("Ticket ID must be a string")
    cleaned = value.strip().upper()
    if not re.fullmatch(r"T\d+", cleaned):
        raise ValidationError("Ticket ID must use format T001, T002, ...")
    ids = {candidate.strip().upper() for candidate in existing_ids}
    if cleaned in ids:
        raise ValidationError(f"Ticket ID '{cleaned}' already exists")
    return cleaned


def validate_ticket(ticket_dict):
    if not isinstance(ticket_dict, dict):
        raise ValidationError("Ticket must be a dictionary")

    normalized = copy.deepcopy(ticket_dict)
    required = [
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
    ]
    missing = [key for key in required if key not in normalized]
    if missing:
        raise ValidationError(f"Ticket is missing required fields: {missing}")

    normalized["id"] = validate_ticket_id(normalized["id"], [])
    normalized["title"] = validate_title(normalized["title"])
    normalized["category"] = validate_category(normalized["category"])
    normalized["urgency"] = validate_urgency(normalized["urgency"])
    normalized["affected_users"] = validate_affected_users(
        normalized["affected_users"]
    )
    normalized["priority"] = str(normalized["priority"]).strip().casefold()
    if normalized["priority"] not in VALID_PRIORITIES:
        raise ValidationError("Priority must be low, medium, high, or critical")
    normalized["status"] = str(normalized["status"]).strip().casefold()
    if normalized["status"] not in VALID_STATUSES:
        raise ValidationError("Status must be open, in_progress, or resolved")
    assigned = normalized["assigned_to"]
    if assigned is not None:
        normalized["assigned_to"] = validate_staff_label(assigned)
    notes = normalized.get("notes", [])
    if notes is None:
        notes = []
    if not isinstance(notes, list):
        raise ValidationError("Notes must be a list")
    seen_note_ids = set()
    normalized_notes = []
    for note in notes:
        if not isinstance(note, dict):
            raise ValidationError("Each note must be a dictionary")
        if set(note.keys()) != {"note_id", "author", "message"}:
            raise ValidationError("Notes must contain note_id, author, and message")
        note_id = str(note["note_id"]).strip().upper()
        if not re.fullmatch(r"N\d+", note_id):
            raise ValidationError("Note IDs must use format N001, N002, ...")
        if note_id in seen_note_ids:
            raise ValidationError(f"Duplicate note ID: {note_id}")
        seen_note_ids.add(note_id)
        normalized_notes.append(
            {
                "note_id": note_id,
                "author": validate_staff_label(note["author"]),
                "message": validate_note_message(note["message"]),
            }
        )
    normalized["notes"] = normalized_notes

    if normalized["priority"] != calculate_priority(
        normalized["urgency"], normalized["affected_users"]
    ):
        raise ValidationError(
            "Priority is inconsistent with urgency and affected_users"
        )

    return normalized


def validate_note_message(message):
    if not isinstance(message, str):
        raise ValidationError("Note message must be a string")
    cleaned = message.strip()
    if len(cleaned) < 5 or len(cleaned) > 300:
        raise ValidationError("Note message must be 5-300 characters after trimming")
    return cleaned


def can_transition(ticket, new_status):
    if not isinstance(ticket, dict):
        raise TransitionError("Ticket must be a dictionary")
    if new_status is None:
        raise TransitionError("New status is required")
    normalized = str(new_status).strip().casefold()
    if normalized not in VALID_STATUSES:
        raise TransitionError(f"Invalid status: {new_status}")

    current = ticket.get("status", "").strip().casefold()
    if current == normalized:
        raise TransitionError(f"Ticket is already {current}")

    if current == "resolved":
        if normalized != "open":
            raise TransitionError("Resolved tickets must be reopened first")
        return

    if normalized == "open":
        raise TransitionError("Use reopen_ticket() to reopen a resolved ticket")

    if normalized == "in_progress":
        if current != "open":
            raise TransitionError("Ticket must be open before work starts")
        if not ticket.get("assigned_to"):
            raise TransitionError("Cannot start work on an unassigned ticket")
        return

    if normalized == "resolved":
        if current != "in_progress":
            raise TransitionError("Only an in-progress ticket can be resolved")
        return

    raise TransitionError(f"Invalid transition: {current} -> {normalized}")
