# Challenge 01 — Movies Search

Amazon-style SDE-1 practice: fix broken search behavior in a Django API used by a React UI.

## Product spec

### Simple search
- User enters a query and picks a field: `all`, `title`, `director`, `description`, or `cast`.
- Results must match the query in the **selected** field (substring, case-insensitive).
- When `all` is selected, match if **any** of those fields contains the query.

### Advanced search
- User may fill multiple filters: title, director, description, cast, genre, year.
- Empty filters are ignored.
- When multiple filters are set, a movie must satisfy **all** of them (logical AND).

## Run

```bash
./run.sh          # API + React UI
./run.sh --agent  # coaching agent (guides, does not give answers)
./test.sh         # acceptance tests
```

- UI: http://127.0.0.1:5173  
- API health: http://127.0.0.1:8000/api/health/

## Your job

Explore the UI, reproduce incorrect results, find and fix the backend logic so `./test.sh` is green.

## Coach rules

`./run.sh --agent` helps with Django/React debugging technique and syntax.
It will **refuse** to name the bug or paste the fixed code.
