def build_report(tickets):
    tickets = tickets or []
    by_status = {"open": 0, "in_progress": 0, "resolved": 0}
    by_priority = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_category = {"Network": 0, "Hardware": 0, "Software": 0, "Other": 0}

    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue
        status = str(ticket.get("status", "")).strip().casefold()
        if status in by_status:
            by_status[status] += 1

        priority = str(ticket.get("priority", "")).strip().casefold()
        if priority in by_priority:
            by_priority[priority] += 1

        category = str(ticket.get("category", "")).strip()
        if category in by_category:
            by_category[category] += 1

    total = len(tickets)
    unresolved = by_status["open"] + by_status["in_progress"]
    resolved = by_status["resolved"]
    resolution_percent = (resolved / total * 100.0) if total else 0.0

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "unresolved": unresolved,
        "resolved": resolved,
        "resolution_percent": resolution_percent,
    }


def format_report(report):
    # Only the report output gets the extra heading; list/search views remain unchanged.
    lines = ["Ticket Report", "", f"Total tickets: {report.get('total', 0)}"]
    lines.append("Status breakdown:")
    for key in ("open", "in_progress", "resolved"):
        lines.append(f"  {key}: {report.get('by_status', {}).get(key, 0)}")
    lines.append("Priority breakdown:")
    for key in ("critical", "high", "medium", "low"):
        lines.append(f"  {key}: {report.get('by_priority', {}).get(key, 0)}")
    lines.append(f"Unresolved: {report.get('unresolved', 0)}")
    lines.append(f"Resolved: {report.get('resolved', 0)}")
    lines.append(f"Resolution percent: {report.get('resolution_percent', 0.0)}%")
    return "\n".join(lines)


def generate_report(tickets: list[dict]) -> dict:
    report = build_report(tickets)
    legacy = {
        "total_tickets": report["total"],
        "status_breakdown": report["by_status"],
        "priority_breakdown": report["by_priority"],
    }
    return {**report, **legacy}
