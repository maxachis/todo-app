## Context

The task page (`/`) renders a three-panel layout with drag-and-drop task lists, keyboard navigation, and conditional navbar components (SearchBar, ExportButton). With a large dataset (e.g., 176 tasks, 112 subtasks), navigation away from the task page sometimes fails — clicking navbar links produces no response.

Key architectural details of the current state:
- **SvelteKit router** intercepts clicks on `document.documentElement` (the `<html>` element) during the bubble phase
- **Svelte 5 event delegation** adds a single click handler on the `document` (one level above `<html>`)
- **svelte-dnd-action@0.9.69** adds `mousedown` listeners to every draggable child element; these handlers call `e.stopPropagation()` and `e.preventDefault()` (for non-touch events)
- **Three `<svelte:window onclick>` handlers** are active on the task page (layout settings, SearchBar, ExportButton) vs. one on other pages
- **TaskList `$effect`** reads and writes `sortableActiveTasks` (a `$state` array), potentially causing re-render cascades with the DnD zone's `configure()` iterating all children on each update

## Goals / Non-Goals

**Goals:**
- Navbar navigation SHALL work reliably from the task page with any data volume
- Identify and fix the specific root cause (event interference, main-thread blocking, or reactive loop)
- Add an E2E regression test that loads a large dataset and verifies navigation

**Non-Goals:**
- Task list virtualization (future perf optimization)
- Replacing svelte-dnd-action
- Changing the three-panel layout architecture

## Decisions

### 1. Diagnostic-first approach: E2E test to reproduce, then targeted fix

**Rationale**: The bug is intermittent and data-dependent. Rather than speculatively refactoring, write an E2E test that loads the large dataset and attempts navigation from the task page. This confirms the exact failure mode (frozen main thread vs. blocked event vs. routing failure) and prevents regression.

**Alternative considered**: Immediately refactoring all `<svelte:window onclick>` handlers. Rejected because this might not fix the actual issue and could introduce regressions in click-outside behavior.

### 2. Use `goto()` on navbar links as the primary fix

**Rationale**: SvelteKit's router intercepts `<a>` clicks via a document-level listener. If any component in the event path calls `stopPropagation()` or `preventDefault()` before the event reaches `document.documentElement`, the router never sees the click. Adding explicit `onclick` handlers with `goto()` on nav links ensures navigation always works regardless of event interference from child components.

**Alternative considered**: Patching svelte-dnd-action to not call `stopPropagation()`. Rejected because it's a library internal and could break DnD behavior.

### 3. Optimize TaskList reactive effect to prevent re-render cascades

**Rationale**: The `$effect` in `TaskList.svelte` reads `sortableActiveTasks` (to detect just-completed tasks) and then writes to it. In Svelte 5, this creates a reactive dependency that can trigger additional effect runs. Each run causes the DnD zone to reconfigure (iterating all children to add/remove event listeners). With 100+ task items, this amplifies into significant main-thread work.

**Fix**: Use `untrack()` for the read of `sortableActiveTasks` to break the reactive dependency loop.

### 4. Scope click-outside handlers to avoid global listeners

**Rationale**: SearchBar and ExportButton each add `<svelte:window onclick>` handlers. While these don't call `stopPropagation()`, having multiple global click handlers increases event processing overhead and complicates the event flow. Replacing with focused `document.addEventListener` in `onMount`/`onDestroy` is cleaner and easier to reason about.

## Risks / Trade-offs

- **[Risk] `goto()` bypasses SvelteKit preloading** → Mitigation: Navbar links don't use preloading, so no functional difference. Can add `preloadData` calls if needed later.
- **[Risk] `untrack()` in TaskList effect might miss legitimate updates** → Mitigation: The `tasks` prop (from parent) is still tracked; only the self-referential read of `sortableActiveTasks` is untracked. Completion detection still works because it compares against `tasks`.
- **[Risk] E2E test with large dataset may be slow** → Mitigation: Use the native import API endpoint to load data, limit to one navigation assertion to keep test fast.
