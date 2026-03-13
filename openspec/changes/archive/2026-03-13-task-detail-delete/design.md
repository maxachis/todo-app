## Context

The task detail panel (`TaskDetail.svelte`) displays fields for editing a selected task but has no delete action. Deletion is only possible via the keyboard shortcut (Backspace/Delete key) handled in `keyboard.ts`. The `deleteTask` store function and `api.tasks.remove` API client already exist and handle store cleanup (removing the task from the list store and clearing selection).

## Goals / Non-Goals

**Goals:**
- Provide a visible delete button in the task detail panel
- Confirm before deleting to prevent accidental loss
- Reuse existing deletion infrastructure (store + API)

**Non-Goals:**
- Soft delete or undo functionality
- Backend changes
- Changing keyboard shortcut behavior

## Decisions

**1. Button placement: bottom of detail panel**
A delete button at the bottom of the form keeps it out of the way of everyday editing while remaining accessible. Alternative: toolbar/header — rejected because the detail panel has no toolbar and adding one for a single action is overkill.

**2. Confirmation via `window.confirm()`**
The existing keyboard delete handler already uses `confirm()`. Using the same mechanism keeps behavior consistent and avoids introducing a custom modal component for a single use case.

**3. Reuse `deleteTask` from tasks store**
The store function already handles API call, list store cleanup, and selection clearing. No new logic needed.

## Risks / Trade-offs

- [Accidental deletion] → Mitigated by confirmation dialog. Consistent with existing keyboard shortcut behavior.
- [Button discoverability vs. clutter] → Placed at bottom with subdued destructive styling so it doesn't dominate the panel.
