## Context

The Dashboard Upcoming tab fetches `GET /api/upcoming/` which returns incomplete tasks filtered by `due_date__isnull=False`. The frontend groups these into time-horizon buckets (Overdue, Today, Tomorrow, This Week, Later). Pinned tasks without due dates are currently invisible on the dashboard.

The `is_pinned` field already exists on the Task model and is returned by the upcoming endpoint. No schema or migration changes are needed on the model level.

## Goals / Non-Goals

**Goals:**
- Surface pinned tasks (including those without due dates) on the Dashboard Upcoming tab
- Show a dedicated "Pinned" group above time-horizon groups

**Non-Goals:**
- Changing pin behavior in the task list view
- Adding new API endpoints

## Decisions

### 1. Extend existing `/api/upcoming/` endpoint vs. new endpoint

**Decision**: Extend the existing endpoint with a union query.

**Rationale**: The upcoming endpoint already returns all the fields needed. Adding a separate endpoint would require the frontend to merge two data sources. Instead, we use `Q(due_date__isnull=False) | Q(is_pinned=True, is_completed=False)` to include pinned tasks without due dates in the same response.

**Alternative considered**: Separate `GET /api/pinned/` endpoint — rejected because it adds frontend complexity for merging and deduplication.

### 2. Make `due_date` nullable in response schema

**Decision**: Change `UpcomingTaskSchema.due_date` from `str` to `str | None` and `UpcomingTask.due_date` from `string` to `string | null`.

**Rationale**: Pinned tasks without due dates will have `due_date: null`. The frontend grouping logic must handle this by routing null-date pinned tasks to the "Pinned" group only.

### 3. Pinned group placement and deduplication

**Decision**: Show a "Pinned" group above time-horizon groups (but below Follow-ups Due). Pinned tasks with due dates appear in BOTH the Pinned group and their time-horizon group.

**Rationale**: Users pin tasks for visibility. Showing them in both places ensures pinned items are prominent while maintaining the complete time-horizon view. This avoids confusion where a due-today pinned task disappears from "Today".

**Alternative considered**: Deduplicate (show pinned tasks only in Pinned group) — rejected because it would hide time-sensitive information from the horizon groups.

### 4. Sort order within Pinned group

**Decision**: Sort by priority descending, then by title alphabetically. Tasks with due dates sort before those without.

**Rationale**: Priority is the most relevant ordering for pinned tasks since they're explicitly flagged. Secondary sort by title provides stable ordering.

## Risks / Trade-offs

- **Duplication**: Pinned tasks with due dates appear twice on the page. This is intentional but could feel redundant. A small visual indicator (pin icon) in the time-horizon rows helps the user understand why.
- **Schema change**: Making `due_date` nullable is a minor breaking change for any code that assumes it's always present. The only consumer is the dashboard frontend, which we're updating simultaneously.
