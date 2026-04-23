# Database setup. Run this once to create the .db file.

import sqlite3
from pathlib import Path

DB_PATH = Path("decay.db")
SCHEMA_PATH = Path("schema.sql")


def connect():
    return sqlite3.connect(DB_PATH)


def setup():
    schema = SCHEMA_PATH.read_text()
    with connect() as conn:
        conn.executescript(schema)
    print(f"Database ready at {DB_PATH}")


if __name__ == "__main__":
    setup()
