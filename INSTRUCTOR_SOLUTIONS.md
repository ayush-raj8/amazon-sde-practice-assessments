# Instructor solution sketches (candidates: do not open)

High-level only — enough to validate a fix without shipping a full patch key in the candidate tree.

## 01-movies-search
- **Simple:** branch on `field`; use `Q` OR across title/director/description/cast when `all`.
- **Advanced:** start from `all()` and **chain** `.filter(...)` per provided dimension (AND), not `|=` on `Q`.

## 02-bookstore-inventory
- Persist `price` on update.
- Apply `category__iexact` when `category` query present.
- `q` → `Q(title__icontains=q) | Q(author__icontains=q)`.

## 03-task-manager
- Apply `status` filter to queryset.
- `mark_complete`: call `save()` after setting status.
- `due_before` → `due_date__lte`.

## 04-employee-directory
- Apply `department__iexact`.
- Name `q` → `name__icontains`.
- Honor `sort` (`name` / `department`) via `order_by`.

## 05-recipe-finder
- Each ingredient → successive `ingredients__icontains` (AND).
- `max_cook_time` → `cook_time_minutes__lte`.
- `diet=vegetarian` → vegetarian **or** vegan.
