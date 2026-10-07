# NM2 — Amazon SDE-1 Practice Assessments (Django + React)

Six self-contained coding challenges modeled on Amazon-style AI-assisted assessments
(including a Django CRUD tutorial with **one project / two apps**).

Each challenge ships with:

- **Django REST** backend (intentional defects)
- **React (Vite)** frontend
- **`./run.sh`** — start API + UI (console-printable URLs)
- **`./test.sh`** — acceptance tests (fail until fixed; pass when correct)
- **`./run.sh --agent`** — Claude-compatible coach that **guides but never gives the answer**

## Quick start

```bash
# pick a challenge
cd challenges/01-movies-search

./run.sh          # UI + API
./test.sh         # see failures, then fix, then green
./run.sh --agent  # coaching mode
```

Full practice guidance: **[CANDIDATE_GUIDE.md](./CANDIDATE_GUIDE.md)**

## Challenges

| # | Folder | Theme | Ports (API / UI) |
|---|--------|-------|------------------|
| 0 | `challenges/00-django-crud-tutorial` | CRUD tutorial (1 project, 2 apps) | 8005 / 5178 |
| 1 | `challenges/01-movies-search` | Simple + advanced movie search | 8000 / 5173 |
| 2 | `challenges/02-bookstore-inventory` | Bookstore CRUD + filters | 8001 / 5174 |
| 3 | `challenges/03-task-manager` | Tasks, status, due dates | 8002 / 5175 |
| 4 | `challenges/04-employee-directory` | Directory search & sort | 8003 / 5176 |
| 5 | `challenges/05-recipe-finder` | Multi-ingredient recipe search | 8004 / 5177 |

## Coach agent

Shared implementation: `shared/coach/agent.py` + `shared/coach/system_prompt.md`.

```bash
./run.sh --agent           # interactive local coach
./run.sh --agent --claude  # prefer Claude CLI if installed
```

The agent refuses answer-territory questions (bug identity, fixed code, spoilers) and helps with Django/React debugging technique.

## Instructor notes

Defect keys live under each challenge’s `.coach/challenge_meta.json` (for the coach / instructors). Do not share that file’s defect section with candidates.

## Requirements

- Python 3.10+ (3.12 recommended)
- Node.js 18+
- npm
