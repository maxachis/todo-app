## Why

Setting a due date when creating a task requires manually interacting with the date picker — even when the task title already contains an obvious date reference like "Buy groceries tomorrow" or "Meeting Jan 15". Automatically detecting dates in the title text and pre-filling the date picker eliminates this redundant step, making the fast "type and Enter" workflow even faster for date-bearing tasks.

## What Changes

- Add `chrono-node` as a frontend dependency for natural language date parsing
- Add date detection logic to `TaskCreateForm` that runs `chrono-node` against the title text on each input event
- Show a dismissible badge next to the date picker when a date is detected, displaying the parsed date in human-readable format
- Pre-fill the existing inline date picker with the detected date (picker remains the single source of truth)
- Implement a three-state detection lifecycle: LISTENING → SHOWING → DISMISSED, resetting on form submission
- When the user types a new date phrase, update the badge and picker to reflect the latest detected date
- When the user manually selects a date in the picker, hide the badge (explicit control takes priority)
- Dismissing the badge (✕) clears the picker and stops detection for the current input session
- Title text is never modified — the date phrase remains in the title as typed

## Capabilities

### New Capabilities

- `smart-date-detection`: Automatic detection of date expressions in the task creation title input, with badge display and date picker pre-fill using chrono-node

### Modified Capabilities

- `inline-task-date`: The date picker now supports being pre-filled programmatically by the detection system, and the badge interacts with the picker's value

## Impact

- **Frontend**: `TaskCreateForm.svelte` gains detection logic, badge UI, and state machine; new `chrono-node` dependency (~40KB gzipped)
- **Backend**: No changes — the existing `due_date` field on the create API is used as-is
- **No breaking changes**: Detection is additive; manual date picker workflow is fully preserved
- **New dependency**: `chrono-node` (npm package for natural language date parsing)
