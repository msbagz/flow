
import json
import os

ticket_dict = {}
FILENAME = "tickets.json"

allowed_categories = ("Network", "Hardware", "Software", "Other")
allowed_urgencies = ("low", "medium", "high")



def validate_title() -> str:
    while True:
        title = input("Ticket title: ").strip()
        if title:
            return title
        print("Title field must not be empty")


def validate_category() -> str:
    while True:
        category = input(
            "Select category (Network, Software, Hardware, Other): "
        ).strip().capitalize()

        if category in allowed_categories:
            return category
        print("Unsupported category. Please try again.")


def validate_urgency() -> str:
    while True:
        urgency = input(
            "Urgency level (high, medium or low): "
        ).strip().lower()

        if urgency in allowed_urgencies:
            return urgency
        print("Invalid urgency. Enter low, medium, or high.")


def validate_affected_users() -> int:
    while True:
        affected_users = input(
            "Number of affected users: "
        ).strip()

        if affected_users.isdigit() and int(affected_users) > 0:
            return int(affected_users)

        print("Entry must be a positive integer greater than 0")


def calculate_priority(urgency: str, affected_users: int) -> str:
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def save_ticket(ticket: dict):
    filename = FILENAME

    if os.path.exists(filename):
        with open(filename, "r") as f:
            all_tickets = json.load(f)

            if isinstance(all_tickets, dict):
                all_tickets = [all_tickets]
    else:
        all_tickets = []

    all_tickets.append(ticket)

    with open(filename, "w") as f:
        json.dump(all_tickets, f, indent=4)


def create_ticket(tickets: list[dict]) -> dict:
    last_num = max(
        (int(ticket["id"][1:]) for ticket in tickets),
        default=0,
    )

    ticket_id = f"T{last_num + 1:03d}"

    ticket = {
        "id": ticket_id,
        "title": validate_title(),
        "category": validate_category(),
        "urgency": validate_urgency(),
        "affected_users": validate_affected_users(),
        "priority": "",
        "status": "open",
        "assigned_to": None,
    }

    ticket["priority"] = calculate_priority(
        ticket["urgency"],
        ticket["affected_users"],
    )

    tickets.append(ticket)

    print(f"Ticket {ticket_id} created successfully.")
    return ticket


def list_tickets(tickets: list[dict]) -> None:
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        for key, value in ticket.items():
            print(f"{key}: {value}")
        print()


def view_ticket(tickets: list[dict]) -> None:
    ticket_id = input("Input ticket ID: ").strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            for key, value in ticket.items():
                print(f"{key}: {value}")
            return

    print("Ticket not found.")