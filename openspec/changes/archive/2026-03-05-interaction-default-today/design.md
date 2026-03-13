## Context

The interaction create form initializes `newDate` to an empty string. After submission, it resets to empty. Users must manually select today's date each time, though most interactions are logged same-day.

## Goals / Non-Goals

**Goals:**
- Default `newDate` to today's date (YYYY-MM-DD) on page load and after form reset

**Non-Goals:**
- Changing backend defaults (already defaults to `timezone.now`)
- Changing edit form behavior

## Decisions

- **Use a `todayStr()` helper**: Create a small inline function returning `new Date().toISOString().slice(0, 10)` for the YYYY-MM-DD format needed by `<input type="date">`.
- **Initialize and reset with it**: Use `todayStr()` for both initial state and post-submit reset.

## Risks / Trade-offs

- None significant. The date is still editable — this just saves a click for the common case.
