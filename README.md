# Decay Graph CRM

A local-first CRM that tracks which of your contacts you haven't reached out to in a while. Leads decay over time without interaction, and the tool shows you who's gone stale.

## Why

Most CRMs track what you've sold. This one tracks which relationships are falling off. Built from real CRM workflow experience. The tools I worked with surfaced conversions, not relationship health. That's backwards for anyone whose business depends on repeat contact.

## Example output

Listing contacts:

```
   1  Alex Chen                       engaged
   2  Jamie Rivera                    new
   3  Morgan Patel                    active
   4  Sam Wu                          dormant
   5  Casey Brown                     closed
```

Staleness view — who you haven't talked to lately:

```
Alex Chen            engaged    1.8 days ago
Jamie Rivera         new        2.8 days ago
Morgan Patel         active     5.8 days ago
Sam Wu               dormant    72.8 days ago   ← stale
Casey Brown          closed     49.8 days ago
```

Sample data from `seed.py`, clearly fictional.

## Status

Day 3. Inspect contacts and see who's gone stale. Actively being built.

## Stack

Python and SQLite. Nothing else yet.

## Usage

```
python3 db.py       # create the database
python3 seed.py     # (optional) load sample mock data so the CLI has something to show

python3 cli.py list                                          # list all contacts
python3 cli.py insert "Maria Garcia" --source "conference"  # add a contact
python3 cli.py log 1 meeting --note "caught up on Q2 plans" # log an interaction
python3 cli.py show 1                                        # contact detail + history
python3 cli.py stale                                         # who's gone quiet
```

`seed.py` inserts clearly fake sample rows (Alex Chen, Jamie Rivera, etc.) for testing and demos. Skip it if you want to start empty.

Insert options: `--status` (new/engaged/active/dormant/closed), `--email`, `--phone`, `--source`, `--notes`

Log kinds: `call`, `email`, `meeting`, `message`, `note`. Use `--date YYYY-MM-DD` to back-date.

`stale` excludes closed contacts and lists everyone else by how long since the last logged interaction. Contacts with no interactions yet show as `never`.

## Roadmap

- [x] Schema and database setup
- [x] Add contacts from the CLI
- [x] Log interactions (calls, emails, meetings)
- [x] Show contact detail + interaction history
- [x] Staleness report (who needs follow-up)
- [ ] Update contact status
- [ ] Graph visualization
- [ ] Lead import from public sources (pluggable interface)

## License

MIT
