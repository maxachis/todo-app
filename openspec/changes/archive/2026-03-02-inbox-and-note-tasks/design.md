## Context

The app has a notebook (daily/wiki pages with mention syntax) and a task system (lists → sections → tasks). There's no quick-capture path from notes to tasks — users must switch to the Tasks view and manually create tasks. The notebook already has a `reconcile_mentions` function that parses content on save to sync `PageEntityMention` and `PageLink` records, so extending it to detect checkbox syntax and create tasks is architecturally natural.

Task lists currently have no concept of "system" vs "user" lists. All lists are equal and fully editable/deletable.

## Goals / Non-Goals

**Goals:**
- System-managed Inbox list that always exists at the top of the sidebar
- Checkbox-to-task creation in notebook saves (`- [ ] text` → task in Inbox)
- List/Section triage fields on the task detail panel for moving tasks between lists

**Non-Goals:**
- Bidirectional sync between note checkboxes and task completion state
- Dedicated triage/inbox-zero UI beyond the existing detail panel
- Subtask creation from notes (all checkbox tasks are top-level)
- Multiple system lists or user-configurable inbox targets

## Decisions

### 1. System list via `is_system` boolean on List model

**Decision**: Add `is_system = BooleanField(default=False)` to the List model. The migration seeds one Inbox list with `is_system=True`, `name="Inbox"`, `emoji="📥"`, `position=0`, and one section with `name=""`.

**Why over alternatives**:
- *Separate InboxList model*: Unnecessary complexity for a single special case. Same table, one flag.
- *Hardcoded ID / slug*: Fragile across environments. A boolean flag is query-friendly (`List.objects.filter(is_system=True).first()`).
- *Position 0 convention without flag*: Can't enforce rename/delete constraints without a marker.

**Constraints enforced**: API update endpoint rejects name changes on system lists (409). API delete endpoint rejects system list deletion (409). Frontend hides rename/delete controls on system lists.

### 2. Single hidden section in Inbox

**Decision**: The Inbox list gets one auto-created section with `name=""`. The frontend suppresses the section header when the section name is empty. The section creation UI is hidden for the Inbox list.

**Why**: Tasks require a section FK. One nameless section gives flat task storage with zero visual clutter. No schema changes needed — just UI logic to hide empty-name section headers.

### 3. Checkbox detection in `reconcile_mentions`

**Decision**: Extend `notebook/mentions.py:reconcile_mentions(page)` to detect the pattern `- [ ] <text>` where `<text>` does NOT contain `[[task:`. For each match, create a task in the Inbox section via the Task model directly (not via API call), then rewrite the line in the page content to `- [ ] [[task:ID|Title]]`. Return the modified content to the caller for persistence.

**Why over alternatives**:
- *Frontend-side detection*: Would require the frontend to call the task API, get the ID back, rewrite content, then save. Race conditions, more network calls, duplicated logic. Server-side keeps it atomic.
- *Separate post-save signal*: Adds indirection. `reconcile_mentions` already mutates related records — adding task creation is a natural extension.
- *Regex pattern*: `^- \[ \] (.+)$` (multiline), skip lines where group 1 matches `\[\[task:`. Simple, no ambiguity.

**Content rewrite flow**:
1. `reconcile_mentions(page)` runs regex over `page.content`
2. For each new checkbox line, creates a Task in the Inbox section
3. Replaces the line text inline: `- [ ] Buy milk` → `- [ ] [[task:42|Buy milk]]`
4. If any replacements were made, saves `page.content` with the rewritten text
5. Existing mention reconciliation then picks up the new `[[task:ID|...]]` patterns

### 4. List/Section fields on TaskDetail

**Decision**: Add two `<select>` elements to `TaskDetail.svelte` — one for list, one for section. Changing the list dropdown loads that list's sections into the section dropdown. Selecting a section triggers `moveTask(taskId, { section_id })`. The list dropdown uses the already-loaded `$listsStore` data; the section dropdown fetches the target list's sections on list change.

**Why**: Consistent with existing detail panel patterns (priority dropdown, tag selector). Works for all tasks, not just Inbox — generally useful for reorganization. No new API endpoints needed; uses existing `moveTask` PATCH.

### 5. Sidebar pinning for Inbox

**Decision**: `ListSidebar.svelte` renders the Inbox list first (above user lists), visually separated by a subtle border. The Inbox is excluded from drag-and-drop reordering. Achieved by filtering: render system lists first, then non-system lists sorted by position.

## Risks / Trade-offs

- **[Content rewriting on save]** → The save flow now modifies content (inserting `[[task:ID|...]]`). If the user is typing while a debounced save fires, the frontend content could diverge from what the server returns. **Mitigation**: The notebook save already returns the updated page object; the frontend should merge the returned content back. The debounce timer (1s) makes mid-edit saves unlikely.

- **[Orphaned tasks]** → If a user deletes the `[[task:ID|...]]` text from a note, the task remains in the Inbox with no note reference. **Mitigation**: This is acceptable — the task was created and now lives in the task system. Deleting a note reference doesn't delete a task. The mention reconciliation will clean up the `PageEntityMention` record naturally.

- **[Migration on existing data]** → The migration inserts a new list at position 0. Existing lists may also have position 0. **Mitigation**: The migration should first increment all existing list positions by 1, then insert the Inbox at position 0.

## Open Questions

None — all decisions resolved during exploration.
