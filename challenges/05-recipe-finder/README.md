# Challenge 05 — Recipe Finder

Amazon-style SDE-1 practice: fix broken recipe search behavior in a Django API used by a React UI.

## Product spec

Search recipes by posting filters to the API:

- **ingredients** (array of strings): a recipe must contain **all** of them as substrings in its ingredients field (logical AND).
- **cuisine** (optional): case-insensitive substring match.
- **diet** (optional): `any` / omitted = no diet filter; `vegetarian` matches vegetarian **or** vegan; `vegan` matches vegan only.
- **max_cook_time** (optional int): recipe `cook_time_minutes` must be **less than or equal** to this value.

## Run

```bash
./run.sh          # API + React UI
./run.sh --agent  # coaching agent (guides, does not give answers)
./test.sh         # acceptance tests
```

- UI: http://127.0.0.1:5177  
- API health: http://127.0.0.1:8004/api/health/

## Your job

Explore the UI, reproduce incorrect results, find and fix the backend logic so `./test.sh` is green.

## Coach rules

`./run.sh --agent` helps with Django/React debugging technique and syntax.
It will **refuse** to name the bug or paste the fixed code.
