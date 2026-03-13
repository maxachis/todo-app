## Context

The app uses svelte-dnd-action (v0.9.69) for drag-and-drop reordering. Each section renders a `DragContainer` component wrapping the task list with a `dndzone` directive. When a section has no tasks, the `{#each}` block renders nothing, leaving the dndzone div with zero height. svelte-dnd-action can't detect a zero-height zone as a valid drop target.

## Goals / Non-Goals

**Goals:**
- Make empty sections accept dropped tasks

**Non-Goals:**
- Changing drag-and-drop library or approach
- Adding visual "drop here" placeholders (CSS min-height is sufficient)

## Decisions

### 1. Add min-height to the dndzone container
Add `min-height: 1.5rem` to the `.task-dnd-zone` CSS class. This gives svelte-dnd-action enough area to register the zone as a valid drop target. The space is small enough not to be visually disruptive but large enough to be a reliable drop target.

**Alternative considered**: Adding a placeholder `<div>` element inside the `{#each}` when empty. Rejected because svelte-dnd-action manages its children internally and injecting non-item elements can cause issues. A CSS-only fix is simpler and more reliable.

### 2. Always apply min-height (not conditional)
Apply the min-height unconditionally rather than only when the section is empty. When tasks exist, the content naturally exceeds 1.5rem anyway, so the min-height has no visual effect. This avoids needing reactive state to track emptiness.

## Risks / Trade-offs

- **[Minimal visual impact]** → 1.5rem of empty space at the bottom of sections is negligible and consistent with existing spacing.
