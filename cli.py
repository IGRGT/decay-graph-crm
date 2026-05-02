# Command-line interface. Run with: python3 cli.py <command>

import argparse
from datetime import datetime
from db import connect


def list_contacts():
    with connect() as conn:
        rows = conn.execute("SELECT id, name, status FROM contacts").fetchall()
    if not rows:
        print("No contacts yet.")
        return
    for contact_id, name, status in rows:
        print(f"{contact_id:>4}  {name:<30}  {status}")


def insert_contact(args):
    with connect() as conn:
        conn.execute(
            "INSERT INTO contacts (name, status, email, phone, source, notes)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (args.name, args.status, args.email, args.phone, args.source, args.notes),
        )
    print(f"Added: {args.name} ({args.status})")


def log_interaction(args):
    occurred = args.date or datetime.now().strftime("%Y-%m-%d")
    with connect() as conn:
        row = conn.execute(
            "SELECT name FROM contacts WHERE id = ?", (args.contact_id,)
        ).fetchone()
        if not row:
            print(f"No contact with id {args.contact_id}.")
            return
        conn.execute(
            "INSERT INTO interactions (contact_id, kind, note, occurred_at)"
            " VALUES (?, ?, ?, ?)",
            (args.contact_id, args.kind, args.note, occurred),
        )
    print(f"Logged {args.kind} with {row[0]} on {occurred}.")


def show_contact(args):
    with connect() as conn:
        contact = conn.execute(
            "SELECT name, status, email, phone, source, notes, created_at"
            " FROM contacts WHERE id = ?",
            (args.contact_id,),
        ).fetchone()
        if not contact:
            print(f"No contact with id {args.contact_id}.")
            return
        interactions = conn.execute(
            "SELECT occurred_at, kind, note FROM interactions"
            " WHERE contact_id = ? ORDER BY occurred_at",
            (args.contact_id,),
        ).fetchall()

    name, status, email, phone, source, notes, created = contact
    print(f"{name} ({status})")
    if email:
        print(f"  email:  {email}")
    if phone:
        print(f"  phone:  {phone}")
    if source:
        print(f"  source: {source}")
    if notes:
        print(f"  notes:  {notes}")
    print(f"  added:  {created[:10]}")
    print()
    if interactions:
        print(f"Interactions ({len(interactions)}):")
        for occurred, kind, note in interactions:
            tail = f"  {note}" if note else ""
            print(f"  {occurred}  {kind:<8}{tail}")
    else:
        print("No interactions yet.")


def stale_report(args):
    with connect() as conn:
        rows = conn.execute(
            "SELECT name, status, days_since_last FROM contact_staleness"
            " WHERE status != 'closed'"
            " ORDER BY (days_since_last IS NULL) DESC, days_since_last DESC"
        ).fetchall()
    if not rows:
        print("No contacts yet.")
        return
    print("Days since last contact:")
    for name, status, days in rows:
        if days is None:
            print(f"  {name:<20} {status:<10} never")
        else:
            print(f"  {name:<20} {status:<10} {int(days):>3} days")


def main():
    parser = argparse.ArgumentParser(description="Decay Graph CRM")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all contacts")

    ins = sub.add_parser("insert", help="Add a new contact")
    ins.add_argument("name")
    ins.add_argument(
        "--status",
        default="new",
        choices=["new", "engaged", "active", "dormant", "closed"],
    )
    ins.add_argument("--email")
    ins.add_argument("--phone")
    ins.add_argument("--source")
    ins.add_argument("--notes")

    log = sub.add_parser("log", help="Log an interaction with a contact")
    log.add_argument("contact_id", type=int)
    log.add_argument("kind", choices=["call", "email", "meeting", "message", "note"])
    log.add_argument("--note")
    log.add_argument("--date", help="YYYY-MM-DD. Defaults to today.")

    show = sub.add_parser("show", help="Show contact detail and interaction history")
    show.add_argument("contact_id", type=int)

    sub.add_parser("stale", help="Show how long since each contact was last reached")

    args = parser.parse_args()

    if args.command == "list" or args.command is None:
        list_contacts()
    elif args.command == "insert":
        insert_contact(args)
    elif args.command == "log":
        log_interaction(args)
    elif args.command == "show":
        show_contact(args)
    elif args.command == "stale":
        stale_report(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
