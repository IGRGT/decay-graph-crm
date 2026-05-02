# Sample data for testing. NOT real contacts. All names and info are made up.
# Run this after `python3 db.py` to populate the database with mock rows,
# so `python3 cli.py` has something to show.

from db import connect

CONTACTS = [
    # (name, status, source, email)
    ("Alex Chen", "engaged", "referral", "alex@example.com"),
    ("Jamie Rivera", "new", "conference", "jamie@example.com"),
    ("Morgan Patel", "active", "inbound", "morgan@example.com"),
    ("Sam Wu", "dormant", "linkedin", "sam@example.com"),
    ("Casey Brown", "closed", "referral", "casey@example.com"),
]

INTERACTIONS = [
    # (contact_id, kind, note, occurred_at)
    (1, "email", "Intro email after meetup", "2026-04-20"),
    (1, "call", "15-min discovery call", "2026-04-22"),
    (2, "email", "Sent pricing deck", "2026-04-21"),
    (3, "meeting", "Weekly sync", "2026-04-15"),
    (3, "call", "Follow-up on proposal", "2026-04-18"),
    (4, "email", "Last outreach, no reply since", "2026-02-10"),
    (5, "note", "Closed, signed contract", "2026-03-05"),
]


def seed():
    with connect() as conn:
        conn.executemany(
            "INSERT INTO contacts (name, status, source, email) VALUES (?, ?, ?, ?)",
            CONTACTS,
        )
        conn.executemany(
            "INSERT INTO interactions (contact_id, kind, note, occurred_at) VALUES (?, ?, ?, ?)",
            INTERACTIONS,
        )
    print(f"Inserted {len(CONTACTS)} mock contacts and {len(INTERACTIONS)} mock interactions.")


if __name__ == "__main__":
    seed()
