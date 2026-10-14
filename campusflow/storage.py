import json
from pathlib import Path

FILENAME = Path("tickets.json")


def load_tickets() -> list[dict]:
    if not FILENAME.exists():
        return []

    try:
        with FILENAME.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {FILENAME}: {error}"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError(
            "tickets.json must contain a list of tickets"
        )

    return tickets


def save_tickets(tickets: list[dict]) -> None:
    with FILENAME.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)
