## Why

After pressing Tab to indent/outdent a task, the `moveTask()` store function refreshes the entire list, causing Svelte to re-render all task row DOM elements. The previously-focused task row element is destroyed and replaced, so focus falls to `document.body`. Since the keyboard action relies on focused task rows to handle arrow keys/j/k, keyboard navigation stops working entirely until the user clicks a task again.

## What Changes

- After Tab indent/outdent operations, re-focus the task row element for the moved task once the DOM has re-rendered
- Ensure `selectedTaskStore` remains set so keyboard navigation continues seamlessly

## Non-goals

- Changing Tab's indent/outdent behavior itself
- Adding new keyboard shortcuts
- Modifying focus behavior for other operations (complete, delete, drag-and-drop)

## Capabilities

### New Capabilities

_(none — this is a bug fix within existing keyboard navigation)_

### Modified Capabilities

- `svelte-frontend`: Fix focus restoration after Tab indent/outdent so keyboard navigation continues working

## Impact

- `frontend/src/lib/actions/keyboard.ts` — Tab handler needs to restore focus after the async indent/outdent completes
- `frontend/src/routes/+page.svelte` — `onIndentTask`/`onOutdentTask` callbacks may need to return a signal or the indent/outdent handler needs post-operation focus logic
