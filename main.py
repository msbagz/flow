from campusflow.errors import (
    NotFoundError,
    StorageError,
    TransitionError,
    ValidationError,
)
from campusflow.notes import add_note, get_notes
from campusflow.reports import build_report, format_report
from campusflow.search import search_tickets, sort_by_priority_then_id
from campusflow.storage import FILENAME, load_tickets, save_tickets
from campusflow.tickets import create_ticket, list_tickets, view_ticket
from campusflow.understanding_check import QUESTION_BANK, run_check
from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_work_queue,
    reopen_ticket,
)


def display_menu(output_fn=print):
    output_fn(
        """
    =========================
        CAMPUS WORKFLOW
    =========================
        1. CREATE TICKET
        2. LIST ALL TICKETS
        3. VIEW TICKET
        4. ASSIGN TICKET TO STAFF
        5. CHANGE STATUS
        6. WORK QUEUE
        7. REPORTS
        8. REOPEN TICKET
        9. EXIT
        10. ADD FOLLOW-UP NOTE
        11. VIEW TICKET NOTES
        12. SEARCH TICKETS
        13. SORTED SEARCH RESULTS
        14. REPORTS (ENHANCED)
        15. ENGINEERING UNDERSTANDING CHECK
    """
    )


def _prompt_valid_choice(input_fn, output_fn, prompt, valid_values):
    while True:
        value = input_fn(prompt).strip()
        if value == "":
            return ""
        if value.casefold() in {item.casefold() for item in valid_values}:
            return value
        output_fn(f"Invalid value. Choose from: {', '.join(valid_values) or 'blank'}")


def main(input_fn=input, output_fn=print, storage_path=None):
    path = storage_path or FILENAME
    try:
        tickets = load_tickets(path)
    except StorageError as error:
        output_fn(f"Could not load tickets: {error}")
        tickets = []

    while True:
        display_menu(output_fn)
        choice = input_fn("Select action: ").strip()

        try:
            if choice == "1":
                create_ticket(tickets)
                save_tickets(path, tickets)

            elif choice == "2":
                list_tickets(tickets, output_fn=output_fn)

            elif choice == "3":
                view_ticket(tickets, input_fn=input_fn, output_fn=output_fn)

            elif choice == "4":
                ticket_id = input_fn("Ticket ID: ").strip().upper()
                staff_name = input_fn("Staff name: ")
                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(path, tickets)
                output_fn("Ticket assigned successfully.")

            elif choice == "5":
                ticket_id = input_fn("Ticket ID: ").strip().upper()
                new_status = input_fn("New status (open/in_progress/resolved): ")
                change_status(tickets, ticket_id, new_status)
                save_tickets(path, tickets)
                output_fn("Ticket status updated successfully.")

            elif choice == "6":
                queue = get_work_queue(tickets)
                if not queue:
                    output_fn("No unresolved tickets.")
                else:
                    for ticket in queue:
                        output_fn(
                            f'{ticket["id"]} | {ticket["priority"]} | {ticket["title"]} | {ticket["status"]}'
                        )

            elif choice == "7":
                report = build_report(tickets)
                output_fn(format_report(report))

            elif choice == "8":
                ticket_id = input_fn("Ticket ID: ").strip().upper()
                reopen_ticket(tickets, ticket_id)
                save_tickets(path, tickets)
                output_fn("Ticket reopened successfully.")

            elif choice == "9":
                output_fn("Goodbye!")
                break

            elif choice == "10":
                ticket_id = input_fn("Ticket ID: ").strip().upper()
                author = input_fn("Author: ")
                message = input_fn("Message: ")
                note = add_note(tickets, ticket_id, author, message)
                save_tickets(path, tickets)
                output_fn(f"Note added: {note['note_id']}")

            elif choice == "11":
                ticket_id = input_fn("Ticket ID: ").strip().upper()
                notes = get_notes(tickets, ticket_id)
                if not notes:
                    output_fn("No notes for this ticket.")
                else:
                    for note in notes:
                        output_fn(f"{note['note_id']} | {note['author']} | {note['message']}")

            elif choice == "12":
                title_query = input_fn("Title contains (blank for any): ").strip()
                category = input_fn("Category (blank for any): ").strip()
                while category and category.casefold() not in {"network", "hardware", "software", "other"}:
                    output_fn("Invalid category. Use Network, Hardware, Software, Other or blank.")
                    category = input_fn("Category (blank for any): ").strip()
                status = input_fn("Status (blank for any): ").strip().casefold()
                while status and status not in {"open", "in_progress", "resolved"}:
                    output_fn("Invalid status. Use open, in_progress, resolved or blank.")
                    status = input_fn("Status (blank for any): ").strip().casefold()
                priority = input_fn("Priority (blank for any): ").strip().casefold()
                while priority and priority not in {"critical", "high", "medium", "low"}:
                    output_fn("Invalid priority. Use critical, high, medium, low or blank.")
                    priority = input_fn("Priority (blank for any): ").strip().casefold()
                results = search_tickets(tickets, title_query, category, status, priority)
                if not results:
                    output_fn("No tickets match the supplied filters.")
                else:
                    for ticket in results:
                        output_fn(f"{ticket['id']} | {ticket['title']} | {ticket['status']} | {ticket['priority']}")

            elif choice == "13":
                title_query = input_fn("Title contains (blank for any): ").strip()
                category = input_fn("Category (blank for any): ").strip()
                while category and category.casefold() not in {"network", "hardware", "software", "other"}:
                    output_fn("Invalid category. Use Network, Hardware, Software, Other or blank.")
                    category = input_fn("Category (blank for any): ").strip()
                status = input_fn("Status (blank for any): ").strip().casefold()
                while status and status not in {"open", "in_progress", "resolved"}:
                    output_fn("Invalid status. Use open, in_progress, resolved or blank.")
                    status = input_fn("Status (blank for any): ").strip().casefold()
                priority = input_fn("Priority (blank for any): ").strip().casefold()
                while priority and priority not in {"critical", "high", "medium", "low"}:
                    output_fn("Invalid priority. Use critical, high, medium, low or blank.")
                    priority = input_fn("Priority (blank for any): ").strip().casefold()
                results = sort_by_priority_then_id(search_tickets(tickets, title_query, category, status, priority))
                if not results:
                    output_fn("No tickets match the supplied filters.")
                else:
                    for ticket in results:
                        output_fn(f"{ticket['id']} | {ticket['title']} | {ticket['status']} | {ticket['priority']}")

            elif choice == "14":
                report = build_report(tickets)
                output_fn(format_report(report))

            elif choice == "15":
                run_check(QUESTION_BANK, input_fn, output_fn, "learning_notes.txt")

            else:
                output_fn("Invalid choice. Select an option between 1 and 15.")

        except (ValidationError, TransitionError, NotFoundError, StorageError, ValueError, OSError) as error:
            output_fn(f"Error: {error}")


if __name__ == "__main__":
    main()