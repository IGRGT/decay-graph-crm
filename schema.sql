-- Decay Graph CRM database schema

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new'
        CHECK(status IN ('new', 'engaged', 'active', 'dormant', 'closed')),
    source TEXT,
    email TEXT,
    phone TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    kind TEXT NOT NULL
        CHECK(kind IN ('call', 'email', 'meeting', 'message', 'note')),
    note TEXT,
    occurred_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);

-- How long it's been since we last talked to each contact.
-- Used for the "who's gone stale" report.
CREATE VIEW IF NOT EXISTS contact_staleness AS
SELECT
    c.id,
    c.name,
    c.status,
    MAX(i.occurred_at) AS last_contact,
    julianday('now') - julianday(MAX(i.occurred_at)) AS days_since_last
FROM contacts c
LEFT JOIN interactions i ON i.contact_id = c.id
GROUP BY c.id;
