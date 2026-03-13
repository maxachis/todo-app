## Context

The task list view has a Pinned section (PinnedSection.svelte) that shows pinned tasks at the top. The `pinnedTasks` derived in `+page.svelte` collects tasks via `sections.flatMap(s => s.tasks).filter(t => t.is_pinned)` — but `s.tasks` only contains top-level tasks. Subtasks live in a nested `subtasks` array within each task. This means pinned subtasks are invisible in the pinned section.

The data is already there — the API serializes `is_pinned` for all tasks including subtasks. The fix is purely in how the frontend collects pinned tasks from the tree.

## Goals / Non-Goals

**Goals:**
- Pinned subtasks (at any nesting depth) appear in the pinned section
- Pinned subtasks show parent context so users know where they live
- Jump-to-task works for pinned subtasks (already works, just needs to be reachable)

**Non-Goals:**
- No grouping of parent+subtask in the pinned section (they appear as independent items)
- No backend changes
- No dashboard changes (already works via direct DB query)

## Decisions

**Recursive collection via helper function**: Add a `collectPinnedTasks` function that walks the task tree depth-first, collecting any task where `is_pinned && !is_completed`. This replaces the flat `flatMap` + `filter`. The helper also builds a `parentTitle` string for subtasks by tracking the ancestor chain.

**Parent context as breadcrumb**: When a pinned task has a parent, display it as "Parent > Subtask" in the pinned section title. For deeply nested tasks, show only the immediate parent to keep it compact (e.g. "Parent > Child" not "Grandparent > Parent > Child").

**Pass parent title as prop**: Rather than modifying the Task type, the `pinnedTasks` derived will produce an enriched array with `{ task, parentTitle }` entries. PinnedSection receives these and conditionally renders the parent prefix.

## Risks / Trade-offs

- **Slight complexity in PinnedSection props** → Minimal; just adding an optional parent title string per entry.
