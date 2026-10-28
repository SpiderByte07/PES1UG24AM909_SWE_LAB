"""Support ticket tracker.

Creates tickets with a priority and category, assigns them to agents,
updates their status, searches and reports on them, and saves them to JSON.
"""
import json
import logging

TICKETS = {}
OPEN_STATUSES = ("open", "in_progress")


def create_ticket(title, description, reporter, *, priority="medium",
                  category="general", audit_log=None):
    """Create a ticket and store it. Return None if the title is empty."""
    if not title:
        return None
    if audit_log is None:
        audit_log = []
    # max(...)+1 avoids id collisions after loading from file.
    ticket_id = str(max((int(k) for k in TICKETS), default=0) + 1)
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "reporter": reporter,
        "assignee": None,
    }
    TICKETS[ticket_id] = ticket
    audit_log.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id, agent):
    """Assign a ticket to an agent. Return False if the ticket is unknown."""
    if ticket_id not in TICKETS:
        return False
    TICKETS[ticket_id]["assignee"] = agent
    return True


def update_status(ticket_id, status):
    """Set a ticket's status. Return the ticket, or None if unknown."""
    if ticket_id not in TICKETS:
        return None
    TICKETS[ticket_id]["status"] = status
    return TICKETS[ticket_id]


def search_tickets(status=None, priority=None):
    """Return tickets matching the given status and/or priority."""
    results = []
    for ticket in TICKETS.values():
        if status is not None and ticket["status"] != status:
            continue
        if priority is not None and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def save_tickets(path="tickets.json"):
    """Write all tickets to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(TICKETS, file)


def load_tickets(path="tickets.json"):
    """Replace the current tickets with those stored in a JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        loaded = json.load(file)
    TICKETS.clear()
    TICKETS.update(loaded)


def print_ticket_report():
    """Print a one-line summary for every ticket."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id):
    """Close a ticket. Return False if the ticket is unknown."""
    return update_status(ticket_id, "closed") is not None


def is_open(ticket_id):
    """Return True if the ticket exists and is open or in progress."""
    ticket = TICKETS.get(ticket_id)
    return ticket is not None and ticket["status"] in OPEN_STATUSES


def main():
    """Run a small demo of the ticket tracker."""
    logging.basicConfig(level=logging.INFO)
    create_ticket("Cannot sign in", "Password reset link fails",
                  "alex@example.com")
    create_ticket("Billing question", "Charged twice", "lee@example.com",
                  priority="high")
    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()
    logging.info("Tickets created: %d", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))
    ticket_id = input("Ticket id to close (Enter to skip): ").strip()
    if ticket_id and not close_ticket(ticket_id):
        print(f"No ticket with id {ticket_id!r}")
    save_tickets()


if __name__ == "__main__":
    main()
