# Challenge 02 — Bookstore Inventory

Amazon-style SDE-1 practice: fix broken inventory behavior in a Django API used by a React UI.

## Product spec

### Books CRUD
- List, create, update, and delete books.
- Fields: `title`, `author`, `isbn`, `price` (decimal), `category`, `stock` (integer).

### List filters
- **Category** (`?category=`): case-insensitive exact match on `category`. Empty means no category filter.
- **Search** (`?q=`): match books whose **title or author** contains the query (case-insensitive substring). Empty means no search filter.
- Both filters may be combined.

### Update
- Updating a book must persist every provided field, including **price** and **stock**.

## Run

```bash
./run.sh          # API + React UI
./run.sh --agent  # coaching agent (guides, does not give answers)
./test.sh         # acceptance tests
```

- UI: http://127.0.0.1:5174  
- API health: http://127.0.0.1:8001/api/health/

## Your job

Explore the UI, reproduce incorrect results, find and fix the backend logic so `./test.sh` is green.

## Coach rules

`./run.sh --agent` helps with Django/React debugging technique and syntax.
It will **refuse** to name the bug or paste the fixed code.
