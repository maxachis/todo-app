# Validation — Fix-Up Round

Tracking table for fix-up implementations. See `TASK-EXECUTION-INSTRUCTIONS.md` for process.

All 88 tests pass after all fix-ups. No regressions.

## Batch 1 Fixes

| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Task count badges | Sidebar OOB swap added to complete/uncomplete/create/delete/move views | Complete a task — badge count decrements immediately without refresh | [ ] | This works with lists, but {n} subtasks collapsible under existing task does not update -- ensure it update and shows n subtasks out of m completed. | 

## Batch 3 Fixes

| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Tab indent | `updateSubtaskCounts()` called after Tab/Shift+Tab | Indent a task with Tab — parent's subtask count label updates immediately | [ ] | |
| Arrow keys | Rewritten to flow between tasks and inputs as unified list | ArrowDown from last task → enters section's input. ArrowUp from input → last task. ArrowDown from input → next section's first task or input. | [ ] | | This works better, but when moving up from the "Add a task section", it successfully moves into the bottommost task, but then I have to press the up key twice -- the first time unfocuses the text box without moving to the next task, and the second time moves to the next task

## Batch 4 Fixes

| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Drag sections | `move_section` rewritten with index-based insertion + sequential renumbering | Drag a section to new position, refresh — order persists | [ ] | This works, but there is a considerable lag immediately after doing this where I cannot perform other interactions |
| Drag lists | `move_list` rewritten (same fix); `sort: false` on child Sortables to prevent interference | Drag a list via sidebar handle, refresh — order persists | [ ] | This still does not work. |
| | Drag handle visible and functional | Hover a sidebar list — handle appears. Drag by handle — list reorders. Click list name — navigates normally. | [ ] |  |

## Batch 5 Fixes

| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Flicker on check-off | Removed `onclick="dismissToast()"`, shortened transition to 0.15s, improved swap timing | Check off a task — smooth fade-out, no flash on re-render | [ ] | Flicker still occurs, |
| | Keyboard shortcut smooth | Focus task, press `x` — same smooth transition as click | [ ] | Flicker still occurs. |
