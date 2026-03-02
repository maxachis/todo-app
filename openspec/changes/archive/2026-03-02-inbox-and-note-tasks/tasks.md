## 1. Backend: System Inbox List

- [x] 1.1 Add `is_system = BooleanField(default=False)` to List model in `tasks/models.py`
- [x] 1.2 Create migration that: (a) adds `is_system` field, (b) increments all existing list positions by 1, (c) creates Inbox list with `name="Inbox"`, `emoji="📥"`, `is_system=True`, `position=0`, and one Section with `name=""`
- [x] 1.3 Add system list guard clauses in `tasks/api/lists.py`: update endpoint rejects name changes on `is_system=True` lists (409), delete endpoint rejects `is_system=True` lists (409), emoji changes remain allowed
- [x] 1.4 Add `is_system` to list serialization schemas in `tasks/api/schemas.py` (both list-level and detail-level responses)

## 2. Backend: Checkbox-to-Task Creation

- [x] 2.1 Add helper function `get_inbox_section()` in `notebook/mentions.py` that returns the Inbox list's section (cache-friendly query: `Section.objects.filter(list__is_system=True).first()`)
- [x] 2.2 Extend `reconcile_mentions(page)` in `notebook/mentions.py` to detect `- [ ] <text>` lines (regex: `^- \[ \] (.+)$` multiline) where text does NOT match `\[\[task:`, create Task in Inbox section, and rewrite line to `- [ ] [[task:ID|Title]]`
- [x] 2.3 Ensure content rewrite is saved to `page.content` before existing mention reconciliation runs, so new `[[task:ID|...]]` patterns are picked up as `PageEntityMention` records

## 3. Frontend: Sidebar Inbox Pinning

- [x] 3.1 Update `ListSidebar.svelte` to render system lists first (filtered from `$listsStore`) above a visual separator, followed by non-system lists sorted by position
- [x] 3.2 Exclude system lists from the drag-and-drop `items` array in `ListSidebar.svelte` so Inbox is not draggable
- [x] 3.3 Update `ListItem.svelte` to hide double-click-to-edit and delete button when `list.is_system === true`
- [x] 3.4 Update center panel header in `+page.svelte` to disable title/emoji double-click editing for system lists

## 4. Frontend: Inbox Section & Creation UI

- [x] 4.1 Update section rendering in `SectionList.svelte` to suppress section header (name, edit, delete controls) when `section.name === ""`
- [x] 4.2 Hide the "Create section" form when the selected list has `is_system === true`

## 5. Frontend: Task Detail List/Section Selectors

- [x] 5.1 Add List `<select>` to `TaskDetail.svelte` populated from `$listsStore`, showing the task's current list as selected
- [x] 5.2 Add Section `<select>` to `TaskDetail.svelte` that shows sections for the selected list; on list change, fetch target list's sections and pre-select the first one
- [x] 5.3 Wire section change to call `moveTask(taskId, { section_id })` and refresh the current list view

## 6. Frontend: Notebook Content Rewrite Handling

- [x] 6.1 Update notebook save flow in `routes/notebook/+page.svelte` to replace local content with the server-returned content after save, so checkbox-to-task rewrites are reflected in the editor without a manual refresh

## 7. API & Store Plumbing

- [x] 7.1 Update `frontend/src/lib/api/types.ts` to add `is_system: boolean` to list types (`TaskList`, `TaskListDetail`)
- [x] 7.2 Ensure `moveTask` in `frontend/src/lib/stores/tasks.ts` triggers a list detail reload when the task moves to a different list (so it disappears from the current view)

## 8. Testing

- [x] 8.1 Add API tests for system list constraints: reject rename, reject delete, allow emoji update (`tasks/tests/test_api_lists.py`)
- [x] 8.2 Add API tests for checkbox-to-task creation: single checkbox, multiple checkboxes, already-linked skipped, checked checkbox skipped (`notebook/tests.py`)
- [x] 8.3 Verify existing task and list API tests still pass after `is_system` field addition
