## Context

The task completion flow:
1. User clicks checkbox → `handleCheck()` in `TaskRow.svelte`
2. `completeTask(taskId)` called in `stores/tasks.ts` → API call → `replaceTaskInList()` updates the task's `is_completed` to `true`
3. `$effect` in `TaskList.svelte` re-filters `sortableActiveTasks` to exclude completed tasks
4. Task is instantly removed from the DnD zone → section height shrinks → scroll container exposes `--bg-page` background

The flash is worst at the bottom of long lists because the scroll position overshoots the new (shorter) content height, revealing the page background.

## Goals / Non-Goals

**Goals:**

- Eliminate the black flash by giving the browser time to smoothly adjust scroll position when a task leaves the active list.

**Non-Goals:**

- Adding Svelte out-transitions (conflicts with `svelte-dnd-action` DOM management).
- Changing scroll container behavior or panel backgrounds.

## Decisions

### Deferred removal via setTimeout in the $effect

**Choice:** In `TaskList.svelte`, when the `$effect` detects a task has become completed (present in old list, absent in new filtered list), delay its removal from `sortableActiveTasks` by 300ms using `setTimeout`. During that delay, the task stays visible with the existing `.completed` styling (opacity 0.5, strikethrough).

**Approach:**

```ts
$effect(() => {
    const activeTasks = tasks
        .filter((t) => !t.is_completed && t.parent_id === null)
        .sort((a, b) => a.position - b.position);

    // Find tasks that just completed (in current list but not in new filtered set)
    const activeIds = new Set(activeTasks.map((t) => t.id));
    const justCompleted = sortableActiveTasks.filter(
        (t) => !activeIds.has(t.id)
    );

    if (justCompleted.length > 0) {
        // Keep completed tasks temporarily, then remove after delay
        const completedInPlace = justCompleted.map((t) => {
            const updated = tasks.find((task) => task.id === t.id);
            return updated ?? t;
        });
        sortableActiveTasks = [...activeTasks, ...completedInPlace];
        setTimeout(() => {
            sortableActiveTasks = activeTasks;
        }, 300);
    } else {
        sortableActiveTasks = activeTasks;
    }
});
```

**Rationale:** 300ms matches the checkbox `check-pop` animation duration (0.3s). The task fades to 0.5 opacity immediately (via the `.completed` class on `TaskRow`), then is removed from the list once the animation finishes. The browser has time to adjust scroll position without an abrupt jump.

**Alternatives considered:**
- *CSS `min-height` on the panel*: Would prevent the shrink but leave dead space permanently.
- *Svelte `out:slide` transition*: Would conflict with `svelte-dnd-action`'s internal DOM management.
- *`requestAnimationFrame` instead of setTimeout*: Only defers one frame (~16ms), not enough for the animation to complete.

## Risks / Trade-offs

- **DnD interaction during delay**: If the user starts dragging within the 300ms window, the "ghost" completed task is still in the DnD zone. Mitigation: completed tasks already have `draggable="false"` in `TaskRow.svelte` (line 206), and the DnD handlers skip completed tasks.
- **Rapid completions**: If the user completes multiple tasks quickly, each triggers a new `setTimeout`. The $effect will re-run and reconcile correctly since it always compares against the latest `tasks` prop.
