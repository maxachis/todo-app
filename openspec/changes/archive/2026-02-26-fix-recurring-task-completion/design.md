## Context

When a recurring task is completed, the current flow is:

1. Frontend calls `POST /tasks/{id}/complete/`
2. Backend marks the task complete, creates next occurrence at `max_pos + 10` (end of section), returns the completed task with `next_occurrence_id`
3. Frontend calls `GET /lists/{id}/` to re-fetch the entire list (full refresh)
4. Frontend shows a toast with "Undo" that calls `POST /tasks/{id}/uncomplete/`

This causes three bugs:
- The full list re-fetch triggers svelte-dnd-action to tear down and rebuild all DND zones, causing a visible blank flash
- The next occurrence appears at the bottom of the section, not in-place
- Undo un-completes the original but leaves the next occurrence as an orphan duplicate

## Goals / Non-Goals

**Goals:**
- Eliminate the page flash on recurring task completion
- Position new occurrence where the completed task was
- Make undo safe for recurring tasks (clean up next occurrence)

**Non-Goals:**
- Changing recurrence date calculation logic
- Adding new recurrence types
- Refactoring DND infrastructure beyond this fix
- Addressing task completion on the Upcoming page (no checkbox there)

## Decisions

### 1. Optimistic store update instead of full list re-fetch

**Decision:** Replace `refreshListDetail()` in `completeTask()` with targeted store mutations.

**Rationale:** The full list re-fetch (`GET /lists/{id}/`) is the root cause of the page flash. Since `svelte-dnd-action` manages its own DOM, receiving an entirely new items array causes it to tear down and rebuild all children. A targeted store update (remove task from active list, insert new occurrence) avoids this because the DND zone's items array is mutated minimally.

**Alternative considered:** Debouncing or batching the store update — rejected because it adds complexity without addressing the core issue (unnecessary full re-fetch).

**Implementation:**
- The `complete` API response already returns the completed task with `next_occurrence_id`
- Extend the response to include the full serialized `next_occurrence` task object
- In the frontend `completeTask()` store function:
  1. Call `replaceTaskInList()` to update the completed task in the store (marks it completed)
  2. If `next_occurrence` exists, call `addTaskToSection()` to insert it
  3. Skip the `refreshListDetail()` call entirely

### 2. Position next occurrence at the completed task's position

**Decision:** Use the completed task's `position` value for the next occurrence instead of `max_pos + 10`.

**Rationale:** The user expects the new occurrence to appear "in place." Using the same position value achieves this naturally since the completed task is filtered out of the active task list by the frontend (moved to the collapsed "Completed" section). No position conflicts arise because the original task is completed and no longer in the active sort order.

**Alternative considered:** Using `position + 1` — rejected because the original task is already filtered out of the active list, so the same position value works correctly.

### 3. Undo cleanup via frontend-orchestrated delete

**Decision:** When undoing a recurring task completion, the frontend will delete the next occurrence (via existing `DELETE /tasks/{id}/`) before calling uncomplete. No new backend endpoint needed.

**Rationale:** The existing `DELETE /tasks/{id}/` endpoint is sufficient. Adding a special parameter to the uncomplete endpoint introduces API complexity for a simple two-step operation. The frontend already has the `next_occurrence_id` from the completion response, so it can orchestrate both calls.

**Alternative considered:** Adding `delete_next_occurrence_id` query param to the uncomplete endpoint — rejected because it couples unrelated concerns (uncomplete + delete) and the frontend can handle this with two sequential calls using existing endpoints.

**Implementation:**
- Store the `next_occurrence_id` in the toast's undo closure
- On undo: `DELETE /tasks/{next_occurrence_id}/` then `POST /tasks/{id}/uncomplete/`
- Update the store accordingly (remove next occurrence, un-complete original)

### 4. API response shape for complete endpoint

**Decision:** Add a `next_occurrence` field (full `TaskSchema` or `null`) to the complete response alongside the existing `next_occurrence_id`.

**Rationale:** The frontend needs the full task data to insert into the store without a separate fetch. Returning it inline eliminates the extra `GET /tasks/{next_occurrence_id}/` call that currently happens.

**Implementation:** In `complete_task` API handler, serialize the next task if it was created and attach it to the response.

## Risks / Trade-offs

- **Store consistency on undo failure** — If the delete-then-uncomplete sequence fails mid-way (delete succeeds but uncomplete fails), the next occurrence is deleted but the original stays completed. → Mitigation: If uncomplete fails after delete, show an error toast. This is an edge case since both operations are simple DB writes on a local SQLite database.

- **Position collisions** — Using the same position for the next occurrence could theoretically conflict if another task has the same position value. → Mitigation: This is already handled by the existing position sort — tasks with equal positions sort stably by creation order. No practical issue.

- **Stale store data** — Skipping `refreshListDetail()` means the store won't pick up changes made outside the current session (e.g., from another browser tab). → Mitigation: This is acceptable for a single-user app. Other operations (list switching, page reload) still trigger full refreshes.
