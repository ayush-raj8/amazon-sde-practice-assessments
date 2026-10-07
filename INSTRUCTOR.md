# Instructor / Author Notes (do not share with candidates)

Defect summaries live in each challenge’s `.coach/challenge_meta.json`.

## Expected starter test results (buggy code)

| Challenge | Expectation |
|-----------|-------------|
| 00-django-crud-tutorial | Campus update / events club filter / cancel URL wiring fail |
| 01-movies-search | Several search tests fail (field ignored; advanced OR) |
| 02-bookstore-inventory | Price update / category / author search fail |
| 03-task-manager | Status filter / mark_complete / due_before fail |
| 04-employee-directory | Department / icontains / sort fail |
| 05-recipe-finder | Ingredient AND / max cook / vegetarian+vegan fail |

After a correct fix, **all** tests in that challenge’s `./test.sh` must pass.

## Coach behavior

`shared/coach/agent.py` + `system_prompt.md` must never reveal defects or paste fixed view code.
Candidates may still ask general Django questions.

## Smoke checklist per challenge

1. `./test.sh` fails on clean checkout (proves bugs exist)
2. Apply known fix → `./test.sh` green
3. `./run.sh` prints UI + API URLs; UI loads
4. `./run.sh --agent` refuses “what is the bug?”
