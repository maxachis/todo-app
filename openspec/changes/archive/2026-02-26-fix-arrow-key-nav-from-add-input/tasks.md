## 1. Add keyboard-scope marker

- [x] 1.1 Add `data-keyboard-scope` attribute to the keyboard-action container `<div>` in `frontend/src/routes/+page.svelte` so TaskCreateForm can find it via DOM traversal

## 2. Handle arrow keys and Escape in TaskCreateForm

- [x] 2.1 Add `onkeydown` handler to the task-add `<input>` in `frontend/src/lib/components/tasks/TaskCreateForm.svelte` that intercepts Arrow Up, Arrow Down, and Escape
- [x] 2.2 On Arrow Up/Down: find the nearest visible `[data-task-id]` element above/below the form by DOM position, blur the input, focus the target task row, and call `selectTask(taskId)`
- [x] 2.3 On Escape: clear the input value (`title = ''`; `dueDate = ''`; `detecting = true`), blur the input, and call `event.stopPropagation()` to prevent the keyboard action from also clearing task selection

## 3. Clear selection on input focus

- [x] 3.1 Add `onfocus` handler to the task-add input that calls `selectTask(null)` to remove the selected-task affordance when the input is focused

## 4. Arrow Down from last task enters add-task input

- [x] 4.1 In `frontend/src/lib/actions/keyboard.ts`, detect when Arrow Down is pressed on the last task in a section (next element is in a different section or doesn't exist) and focus that section's `.create-form .task-input` instead of staying on the same task
- [x] 4.2 Clear task selection (`onSelectTask(null)`) when focusing the add-task input from keyboard navigation

## 5. Verify

- [x] 5.1 Manual test: click "Add task..." input, press Arrow Up — task immediately above the input is selected, further arrow keys continue working
- [x] 5.2 Manual test: click "Add task..." input, press Arrow Down — task immediately below the input (next section) is selected
- [x] 5.3 Manual test: Arrow Down on last task in a section — add-task input is focused, selection cleared
- [x] 5.4 Manual test: Arrow Up from add-task input back to last task, then Arrow Down back to input — full cycle works
- [x] 5.5 Manual test: type text in add-task input, press Escape — input cleared and blurred
- [x] 5.6 Manual test: confirm arrow keys in task detail title input, notes textarea, and search bar still behave normally
