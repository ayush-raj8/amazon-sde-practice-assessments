# Challenge 04 — Employee Directory

Amazon-style SDE-1 practice: fix broken directory search behavior in a Django API used by a React UI.

## Product spec

### Employee list (`GET /api/employees/`)
- Optional `department` — case-insensitive exact match on department.
- Optional `q` — case-insensitive substring match on **name**.
- Optional `sort` — `name` or `department` (default: `name`, ascending).

Filters combine: when both `department` and `q` are set, results must satisfy both.

## Run

```bash
./run.sh          # API + React UI
./run.sh --agent  # coaching agent (guides, does not give answers)
./test.sh         # acceptance tests
```

- UI: http://127.0.0.1:5176  
- API health: http://127.0.0.1:8003/api/health/

## Your job

Explore the UI, reproduce incorrect results, find and fix the backend logic so `./test.sh` is green.

## Coach rules

`./run.sh --agent` helps with Django/React debugging technique and syntax.
It will **refuse** to name the bug or paste the fixed code.
