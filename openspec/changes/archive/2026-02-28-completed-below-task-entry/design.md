## Context

Each section in the Tasks view renders its content via `SectionList.svelte`, which places a `TaskList` component (containing both active and completed tasks) followed by a `TaskCreateForm`. Inside `TaskList.svelte`, the completed tasks collapsible section renders after the active tasks drag container. This means the visual order is: Active Tasks → Completed → Create Form.

## Goals / Non-Goals

**Goals:**
- Move the completed tasks section below the task creation form so the input stays close to active work.

**Non-Goals:**
- Changing completed task styling, collapse state, or count display.
- Modifying drag-and-drop or keyboard navigation behavior.
- Changing the task creation form itself.

## Decisions

**Extract completed section from TaskList into SectionList**: Rather than passing ordering flags into TaskList, the completed tasks rendering will be moved out of `TaskList.svelte` and into `SectionList.svelte`, placed after `TaskCreateForm`. This keeps TaskList focused on active tasks and makes the ordering explicit in the parent layout.

- **Alternative considered**: Add a prop to TaskList to control completed position. Rejected because it adds complexity for a permanent layout change — simpler to restructure the component hierarchy.

**Completed section becomes its own block in SectionList**: The completed tasks data (filtered list, show/hide toggle, count) will be derived in SectionList and rendered inline, or extracted to a small `CompletedTasks` component. The collapsible toggle and task rows reuse existing patterns.

## Risks / Trade-offs

- [Component coupling] Moving completed rendering to SectionList means SectionList needs access to completed task data → Mitigation: TaskList already receives all tasks; pass completed tasks as a separate filtered set or expose from the store.
- [Visual continuity] Users accustomed to current layout may be briefly disoriented → Mitigation: Minimal change, completed section retains same styling and collapse behavior.
