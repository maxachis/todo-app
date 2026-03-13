## Context

`TaskDetail.svelte` uses a `$effect` that watches the reactive `task` prop (derived from `$selectedTaskDetail` store) and resets all local form state variables (`titleValue`, `dueDateValue`, `priorityValue`, `notesValue`) whenever `task` changes:

```js
$effect(() => {
    if (task) {
        titleValue = task.title;
        dueDateValue = task.due_date ?? '';
        priorityValue = task.priority;
        notesValue = task.notes;
        // ...
    }
});
```

This effect runs on every task object mutation — including after the store updates from a successful save. When the user clears the due date, the async `saveDueDate()` calls `await updateTask(...)`, the store updates with the API response (new task object), the `$effect` re-fires, and local values are reset. If the API response arrives while the input still holds the cleared value, or if there's any re-render trigger, the date snaps back.

## Goals / Non-Goals

**Goals:**
- Local form values should only reset when the user switches to a **different task** (task ID changes)
- Store-triggered updates after a save should NOT overwrite in-progress local edits

**Non-Goals:**
- Changing the save-on-blur/change pattern
- Handling concurrent edits from multiple sources (single-user app)
- Optimistic updates in the task store

## Decisions

### Track task ID instead of full task object

Replace the blanket `$effect` that watches the entire `task` object with one that only fires when the task ID changes. Use a local `prevTaskId` variable to detect ID transitions.

**Rationale**: The effect's purpose is to initialize form state when navigating between tasks — it should not run when the same task is updated in the store. Tracking the ID precisely captures the "switched to a different task" intent.

**Alternative considered**: Debouncing or guarding the effect with a "saving" flag. Rejected — adds complexity and race conditions. The ID-tracking approach is simple and correct.

### Keep the effect for side-effect calls

The effect also calls `loadAvailableTags`, `loadLinkedEntities`, and `initListSection`. These should still run only on task ID change, which is the same trigger — so they stay in the same effect.

## Risks / Trade-offs

- **External updates not reflected**: If the backend changes a field value (e.g., recurrence adjusts the date), the local form won't pick it up until the user navigates away and back. This is acceptable for a single-user app and matches how title/notes already behave (they only update on initial load).
