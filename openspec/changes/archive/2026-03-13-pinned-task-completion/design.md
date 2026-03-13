## Context

The PinnedSection component displays high-priority pinned tasks at the top of the center panel on the Tasks page. Currently, each pinned row is a single `<button>` that jumps to the task in its section. There is no way to complete a task directly from this view — users must scroll to the task row or use the detail panel.

The Dashboard already has a separate completion checkbox implementation (per `dashboard-task-completion` spec). This change adds similar functionality to the Tasks page pinned section.

## Goals / Non-Goals

**Goals:**
- Add a completion checkbox to each pinned task row
- Checkbox click completes the task without triggering jump-to-task navigation
- Completed tasks disappear from the pinned section naturally (existing filter excludes completed tasks)

**Non-Goals:**
- No undo toast (the existing uncomplete flow in task detail suffices)
- No changes to the Dashboard pinned group
- No strikethrough animation or delay before removal

## Decisions

**1. Checkbox placement: left side of row, before title**

The checkbox sits at the start of the row, consistent with task rows in sections and on the dashboard. This is the standard position users expect.

**2. Stop propagation on checkbox click**

The pinned row's `onclick` handler jumps to the task. The checkbox click handler calls `event.stopPropagation()` to prevent the jump behavior when completing a task.

**3. Reuse existing `completeTask` store function**

No new API calls or store logic needed. The existing `completeTask` function handles API calls, optimistic updates, recurrence, and store synchronization. The pinned section's derived state automatically excludes completed tasks.

## Risks / Trade-offs

**[Double-click race]** → User could double-click and trigger completion twice. Mitigated by the task disappearing from the list immediately via the reactive filter, and by the API being idempotent for already-completed tasks.
