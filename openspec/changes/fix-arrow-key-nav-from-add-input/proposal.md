## Why

After clicking into a task-add input ("Add task..." / "Add subtask..."), pressing Arrow Up or Arrow Down does nothing — keyboard navigation is completely blocked. The user must click on a task row to restore arrow-key navigation. This breaks click-to-keyboard continuity (FR-KEYBOARD-NAV, scenario "Click-to-keyboard continuity") and makes the keyboard-centric workflow feel broken whenever the add-task input is touched.

## What Changes

- Modify the keyboard action's text-entry guard (`isTextEntryTarget` in `keyboard.ts`) so that Arrow Up/Down keypresses inside the task-add input blur the input and trigger task navigation instead of being swallowed.
- The fix should only apply to the task-create input (`.task-input` inside `.create-form`); other text-entry fields (task detail title, notes textarea, search) must continue to suppress arrow-key navigation as they do today.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities

- `svelte-frontend`: The keyboard navigation requirement's "Click-to-keyboard continuity" scenario should extend to cover focus transitions from the task-add input — pressing Arrow Up/Down while the add-task input is focused should navigate to the nearest task.

## Impact

- **Code**: `frontend/src/lib/actions/keyboard.ts` (text-entry guard logic) and possibly `frontend/src/lib/components/tasks/TaskCreateForm.svelte` (keydown handler to blur + delegate).
- **Specs**: Minor delta to `svelte-frontend` spec (keyboard navigation section).
- **Risk**: Low — scoped to a single keyboard guard path with no API or data model changes.
