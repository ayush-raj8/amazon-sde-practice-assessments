# Challenge 03 — Task Manager

Amazon-style SDE-1 practice: fix broken task filtering and completion in a Django API used by a React UI.

## Product spec

### Task fields
- `title` (string)
- `description` (string)
- `status`: `todo` | `doing` | `done`
- `priority`: `low` | `medium` | `high`
- `due_date`: `YYYY-MM-DD` or null

### API behavior
- **List** tasks with optional query filters:
  - `status` — exact match
  - `priority` — exact match
  - `due_before` — include tasks whose `due_date` is on or before that date
- **Create** a task
- **Update** a task (e.g. change priority)
- **Mark complete** — `POST` sets `status` to `done` and persists it
- **Delete** a task

## Run

```bash
./run.sh          # API + React UI
./run.sh --agent  # coaching agent (guides, does not give answers)
./test.sh         # acceptance tests
```

- UI: http://127.0.0.1:5175  
- API health: http://127.0.0.1:8002/api/health/

## Your job

Explore the UI, reproduce incorrect results, find and fix the backend logic so `./test.sh` is green.

## Coach rules

`./run.sh --agent` helps with Django/React debugging technique and syntax.
It will **refuse** to name the bug or paste the fixed code.
