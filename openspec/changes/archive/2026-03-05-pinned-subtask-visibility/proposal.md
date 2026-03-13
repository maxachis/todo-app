## Why

When a subtask is pinned, it doesn't appear in the Pinned section at the top of the task list view. The pinned section collects tasks via `sections.flatMap(s => s.tasks)`, which only yields top-level tasks — subtasks are nested inside `subtasks` arrays and never reach the filter. This means pinning a subtask appears to do nothing, since the pin icon toggles but the task never shows up in the pinned section.

## What Changes

- Recursively collect pinned tasks from the full task tree (including all nesting depths) when building the pinned section
- When a pinned subtask appears in the pinned section, show its parent context (e.g. "Parent > Subtask") so users can identify where it lives in the hierarchy
- The jump-to-task behavior already works for subtasks (they have `data-task-id` in the DOM), so no change needed there

## Non-goals

- No changes to the pin limit logic (subtasks already count toward the 3-per-list limit, which is fine)
- No changes to the dashboard pinned group (it uses the `/api/upcoming/` endpoint which queries `Task.objects.filter(is_pinned=True)` directly — subtasks are already included)
- No backend changes needed

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `svelte-frontend`: The pinned section must recursively collect pinned tasks from all nesting levels, not just top-level tasks. Pinned subtasks should display with parent context.

## Impact

- **Frontend**: `frontend/src/routes/+page.svelte` — change `pinnedTasks` derived to recurse into subtask trees
- **Frontend**: `frontend/src/lib/components/tasks/PinnedSection.svelte` — display parent context for subtasks
