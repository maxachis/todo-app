## Why

There's no quick-capture path from notebook notes into the task system. When jotting ideas in daily or wiki pages, you have to context-switch to the Tasks view to create a task. An always-present Inbox list acts as a universal landing pad — and checkbox syntax in notes (`- [ ]`) creates tasks instantly without leaving the editor.

## What Changes

- Add a **system Inbox list** — auto-created via migration, always pinned at position 0 in the sidebar, rename-locked, non-deletable, with a single hidden section for flat task storage.
- Add **checkbox-to-task creation** in the notebook editor — on save, `- [ ] <text>` lines (that don't already contain a `[[task:...]]` link) create a task in the Inbox and rewrite the line to `- [ ] [[task:ID|Title]]`. One-directional: the note creates the task, no further sync.
- Add **List/Section fields to TaskDetail** — dropdown selectors for list and section on every task's detail panel, enabling triage (moving tasks out of Inbox into the right list and section) without drag-and-drop.

## Capabilities

### New Capabilities
- `inbox-system-list`: System-managed Inbox list (migration-created, pinned at top, rename-locked, non-deletable, single hidden section)
- `note-checkbox-tasks`: Checkbox syntax detection in notebook content that auto-creates tasks in the Inbox on save

### Modified Capabilities
- `notebook-core`: Mention reconciliation extended to detect `- [ ]` pattern and create tasks via API
- `svelte-frontend`: TaskDetail panel gains List/Section selector fields; ListSidebar pins Inbox at position 0 with distinct visual treatment
- `django-api`: List model gains `is_system` flag; delete/update endpoints enforce system list constraints

## Non-goals

- Bidirectional checkbox sync (checking off `- [x]` in a note does NOT complete the task, and vice versa)
- Bulk triage UI or dedicated Inbox triage view — standard detail-panel editing is sufficient
- Subtask creation from notes — checkboxes always create top-level tasks in the Inbox section

## Impact

- **Backend**: New migration adding `is_system` field to List model and seeding the Inbox list + section. Update and delete endpoints need guard clauses for system lists. Mention reconciliation in `notebook/mentions.py` gains task-creation logic.
- **Frontend**: `ListSidebar.svelte` sorts Inbox first with visual separator. `TaskDetail.svelte` adds List/Section dropdowns. Notebook save flow extended to handle content rewriting after task creation.
- **API**: New task creation calls from the notebook save path (server-side, inside `reconcile_mentions`).
