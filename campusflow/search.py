import copy

from campusflow.validation import ticket_id_number

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def search_tickets(tickets, title_query="", category="", status="", priority=""):
    if tickets is None:
        return []
    title_filter = str(title_query or "").strip().casefold()
    category_filter = str(category or "").strip().casefold()
    status_filter = str(status or "").strip().casefold()
    priority_filter = str(priority or "").strip().casefold()

    results = []
    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue
        title = str(ticket.get("title", "")).strip().casefold()
        if title_filter and title_filter not in title:
            continue
        if category_filter and category_filter != str(ticket.get("category", "")).strip().casefold():
            continue
        if status_filter and status_filter != str(ticket.get("status", "")).strip().casefold():
            continue
        if priority_filter and priority_filter != str(ticket.get("priority", "")).strip().casefold():
            continue
        results.append(copy.deepcopy(ticket))
    return results


def sort_by_priority_then_id(results):
    return sorted(
        results,
        key=lambda ticket: (
            PRIORITY_ORDER.get(str(ticket.get("priority", "low")).strip().casefold(), 99),
            ticket_id_number(ticket.get("id", "T0")),
        ),
    )
