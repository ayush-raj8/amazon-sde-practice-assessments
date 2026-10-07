# Candidate Practice Guide — Amazon-style SDE-1 (Django + React)

This monorepo simulates an Amazon AI-assisted coding assessment: a small product with **intentional defects**, a **React UI**, a **Django API**, automated **tests**, and a **coach agent** that helps you debug without handing you the answer.

## What interviewers are scoring

1. Can you reproduce the bug from the product spec + UI?
2. Can you trace request → view → queryset → response?
3. Can you use tests as the acceptance contract?
4. Do you fix root cause (not paper over symptoms)?
5. Can you use an AI assistant *as a coach* without outsourcing the solution?

## How a challenge works

| Step | Action |
|------|--------|
| 1 | `cd challenges/<name>` |
| 2 | Read `README.md` (product spec only — no spoilers) |
| 3 | `./run.sh` — open the UI URL printed in the console |
| 4 | Click through the broken flows; note unexpected results |
| 5 | `./test.sh` — see which acceptance tests fail |
| 6 | Inspect `backend/*/views.py` (and related modules) |
| 7 | Optional: `./run.sh --agent` for guided debugging |
| 8 | Fix until `./test.sh` is fully green |
| 9 | Re-check the UI manually |

## Coach agent rules (important)

```bash
./run.sh --agent
```

The coach **will**:

- Explain Django ORM / views / DRF / React fetch concepts
- Suggest debugging steps (Network tab, Django shell, print queryset SQL)
- Ask what you observed vs expected

The coach **will refuse**:

- “What is the bug?”
- “Fix it for me”
- “Paste the correct code”
- Confirming your exact one-line patch as “yes that’s it”

If you only ask for answers, you are practicing the wrong skill.

## Recommended practice order

1. **01-movies-search** — fielded simple search + multi-filter AND (classic)
2. **02-bookstore-inventory** — CRUD + list filters
3. **03-task-manager** — status filters + persistence bugs
4. **04-employee-directory** — search / sort / department filter
5. **05-recipe-finder** — multi-ingredient AND + diet + cook-time bounds

## Debugging checklist (use every time)

1. Reproduce in UI with a concrete example (write expected titles/ids down).
2. Copy the failing HTTP call (method, URL, query/body) from DevTools → Network.
3. Hit the same call with `curl` or DRF browsable API / httpie.
4. Open the view; list every request field the product requires.
5. For each field, ask: is it read? is it applied to the queryset? is the lookup right (`icontains` vs exact, `lte` vs `gte`)?
6. For multi-filter features: are conditions ANDed or ORed? Does that match the README?
7. For mutations: is `.save()` called? Are all fields in the serializer/`validated_data`?
8. Run `./test.sh` after each meaningful change.

## Django syntax refreshers (general — not challenge spoilers)

```python
# Case-insensitive substring
Model.objects.filter(title__icontains=q)

# Multiple kwargs = AND
Model.objects.filter(director__icontains=d, genre__icontains=g)

# OR with Q
from django.db.models import Q
Model.objects.filter(Q(title__icontains=q) | Q(director__icontains=q))

# Chain filters = AND
qs = Model.objects.all()
if d:
    qs = qs.filter(director__icontains=d)
if g:
    qs = qs.filter(genre__icontains=g)
```

## Timeboxing suggestion

| Challenge | Solo target |
|-----------|-------------|
| Movies | 45–60 min |
| Bookstore | 40–50 min |
| Task manager | 40–50 min |
| Employees | 35–45 min |
| Recipes | 45–60 min |

If stuck >15 minutes, use the coach for **process**, not the patch.

## Ports (run one challenge at a time, or all if ports free)

| Challenge | API | UI |
|-----------|-----|----|
| 01-movies-search | 8000 | 5173 |
| 02-bookstore-inventory | 8001 | 5174 |
| 03-task-manager | 8002 | 5175 |
| 04-employee-directory | 8003 | 5176 |
| 05-recipe-finder | 8004 | 5177 |

## Done criteria

A challenge is complete when:

- `./test.sh` exits 0
- Manual UI checks match the README product spec
- You can explain your fix in 60 seconds without reading the diff
