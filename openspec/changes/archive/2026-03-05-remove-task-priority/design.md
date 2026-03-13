## Context

Priority is an integer field on the Task model (0=None, 1=Low, 3=Medium, 5=High). It appears in:
- Task detail panel as a `<select>` dropdown
- Dashboard task rows as colored badges (Low/Med/High)
- Dashboard pinned tasks sorting (priority desc as tiebreaker)
- API schemas for task CRUD and upcoming endpoint
- TickTick CSV import and full backup export/import
- Two test files

The field has a migration (`0003_task_created_at_task_due_time_task_priority`). Since migrations are append-only, we add a new migration to remove the column rather than editing the existing one.

## Goals / Non-Goals

**Goals:**
- Completely remove priority from model, API, frontend, and tests
- Clean migration that drops the column

**Non-Goals:**
- Preserving priority data (user confirmed it's unused)
- Adding alternative sorting/ranking

## Decisions

### 1. Django migration to remove the field
Add a new migration that removes the `priority` column. Django's `makemigrations` will auto-detect the field removal.

### 2. Remove rather than hide
Since priority is unused, fully remove all code rather than just hiding the UI. This avoids dead code and keeps the codebase clean.

### 3. Dashboard pinned sorting fallback
Currently pinned tasks sort by priority desc, then due date, then title. With priority removed, sort by due date presence, then due date asc, then title — which is the natural fallback.

### 4. Import backward compatibility
Full backup import: silently ignore `priority` key if present in imported JSON (for old exports). TickTick import: stop reading the Priority column.

## Risks / Trade-offs

- **[Old exports]** → Full import will silently skip `priority` field if present. No data loss since we're removing the feature.
- **[Migration on production]** → Simple column drop, low risk. SQLite handles this cleanly.
