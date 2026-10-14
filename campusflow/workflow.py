import copy

from campusflow.errors import NotFoundError, TransitionError
from campusflow.validation import can_transition, ticket_id_number, validate_staff_label


def assign_ticket(tickets: list[dict], ticket_id: str, staff_name: str) -> dict:
    if tickets is None:
        raise NotFoundError("Tickets collection is missing")
    cleaned_id = str(ticket_id or "").strip().upper()
    if not str(staff_name or "").strip():
        raise ValueError("Staff name cannot be empty")
    try:
        cleaned_name = validate_staff_label(staff_name)
    except ValueError as exc:
        raise ValueError("Staff name cannot be empty") from exc

    for ticket in tickets:
        if ticket.get("id") == cleaned_id:
            if ticket.get("status", "").strip().casefold() == "resolved":
                raise TransitionError("Reopen the ticket before modifying it")
            ticket["assigned_to"] = cleaned_name
            return ticket

    raise NotFoundError(f"Ticket '{cleaned_id}' not found")


def change_status(tickets: list[dict], ticket_id: str, new_status: str) -> dict:
    if tickets is None:
        raise NotFoundError("Tickets collection is missing")
    cleaned_id = str(ticket_id or "").strip().upper()
    cleaned_status = str(new_status or "").strip().casefold()

    for ticket in tickets:
        if ticket.get("id") == cleaned_id:
            can_transition(ticket, cleaned_status)
            ticket["status"] = cleaned_status
            return ticket

    raise NotFoundError(f"Ticket '{cleaned_id}' not found")


def get_work_queue(tickets: list[dict]) -> list[dict]:
    if not tickets:
        return []
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    unresolved = [
        ticket for ticket in tickets if ticket.get("status", "").strip().casefold() in {"open", "in_progress"}
    ]
    return sorted(
        unresolved,
        key=lambda ticket: (
            priority_order.get(str(ticket.get("priority", "low")).strip().casefold(), 99),
            ticket_id_number(ticket.get("id", "T0")),
        ),
    )


def reopen_ticket(tickets: list[dict], ticket_id: str) -> dict:
    if tickets is None:
        raise NotFoundError("Tickets collection is missing")
    cleaned_id = str(ticket_id or "").strip().upper()
    for ticket in tickets:
        if ticket.get("id") == cleaned_id:
            if ticket.get("status", "").strip().casefold() != "resolved":
                raise TransitionError("Only resolved tickets can be reopened")
            ticket["status"] = "open"
            return ticket
    raise NotFoundError(f"Ticket '{cleaned_id}' not found")