# Command-line interface. Run with: python cli.py

from db import connect


def list_contacts():
    with connect() as conn:
        rows = conn.execute("SELECT id, name, status FROM contacts").fetchall()
    if not rows:
        print("No contacts yet.")
        return
    for contact_id, name, status in rows:
        print(f"{contact_id:>4}  {name:<30}  {status}")


if __name__ == "__main__":
    list_contacts()
