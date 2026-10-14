def generate_report(tickets: list[dict]) -> dict:
    statuses = ("open", "in_progress", "resolved")
    priorities = ("critical", "high", "medium", "low")

    status_breakdown = {
        status: sum(
            ticket["status"] == status for ticket in tickets
        )
        for status in statuses
    }

    priority_breakdown = {
        priority: sum(
            ticket["priority"] == priority for ticket in tickets
        )
        for priority in priorities
    }

    return {
        "total_tickets": len(tickets),
        "status_breakdown": status_breakdown,
        "priority_breakdown": priority_breakdown,
    }