# Validation

Tracking table for current TODO.md implementations. See `TASK-EXECUTION-INSTRUCTIONS.md` for process.

All 88 tests pass. No regressions.

## Fix-Up: List Order Persist Bug (sortable_init.js)

| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Updating list order does not persist on refresh | **Two bugs fixed:** (1) Removed nested child Sortables on `.list-nav-item`; single `#list-nav` Sortable now handles both list reordering and cross-list task drops. (2) Added `.order_by("position")` to `_get_lists_with_counts()` in `lists.py` — Django's `annotate()` was silently dropping the model's default Meta ordering, causing the sidebar to render lists in arbitrary order despite correct DB positions. | 1. Drag a list by its handle to a new position. 2. Verify it stays in the new position. 3. Refresh (F5) — order persists. 4. Click a list after dragging — navigation works normally. 5. Drag a task from center panel onto a sidebar list — task moves to that list. | [ ] | |
