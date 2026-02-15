# Validation

Tracking table for current TODO.md implementations. See `TASK-EXECUTION-INSTRUCTIONS.md` for process.

All 88 tests pass. No regressions.

## Batch 1 (parallel)

### Agent A: List Order Persist Bug (sortable_init.js)

| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Updating list order does not persist on refresh | Added `onStart` click blocker + `onEnd` cleanup to list drag Sortable — prevents spurious HTMX click (hx-get) after drag-end from overwriting reordered sidebar | 1. Create 3+ lists. 2. Drag a list to a new position by its handle. 3. Verify it stays in the new position. 4. Refresh (F5) — order persists. 5. Click a list after dragging — normal click navigation works. | [ ] | Does not work. |

