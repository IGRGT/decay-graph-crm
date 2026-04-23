# Decay Graph CRM

A local-first CRM that tracks which of your contacts you haven't reached out to in a while. Leads decay over time without interaction, and the tool shows you who's gone stale.

## Why

Most CRMs track what you've sold. This one tracks which relationships are falling off. Built from real CRM workflow experience. The tools I worked with surfaced conversions, not relationship health. That's backwards for anyone whose business depends on repeat contact.

## Status

Day 1. Schema in place, database setup works, CLI lists contacts (empty for now). Actively being built.

## Stack

Python and SQLite. Nothing else yet.

## Usage

```
python db.py      # creates the database file
python cli.py     # lists contacts
```

## Roadmap

- [x] Schema and database setup
- [ ] Add, update, and delete contacts
- [ ] Log interactions (calls, emails, meetings)
- [ ] Staleness report (who needs follow-up)
- [ ] Graph visualization
- [ ] Lead import from public sources (pluggable interface)

## License

MIT
