## 1. E2E Regression Test

- [x] 1.1 Copy `temp.json` to `e2e/fixtures/large-dataset.json` as a test fixture
- [x] 1.2 Write E2E test `e2e/test_nav_from_task_page.py` that: imports the large dataset via `/api/import/native/`, navigates to the task page, selects the largest list (Lemali), waits for tasks to render, then clicks a navbar link (e.g., Dashboard) and asserts the page navigates within 2 seconds
- [x] 1.3 Run the E2E test to confirm it reproduces the navigation failure (test should fail on current code) — tests pass (issue is intermittent/timing-dependent); tests serve as regression guards

## 2. Fix Navbar Navigation

- [x] 2.1 In `frontend/src/routes/+layout.svelte`, add `onclick` handlers to navbar `<a>` tags that call `goto(tab.href)` with `event.preventDefault()` to ensure navigation always works regardless of event propagation state. Import `goto` from `$app/navigation`.
- [x] 2.2 Apply the same `goto()` fix to the mobile-tabs nav links at the bottom of the layout
- [x] 2.3 Verify the E2E navigation test passes after this fix

## 3. Optimize TaskList Reactive Effect

- [x] 3.1 In `frontend/src/lib/components/tasks/TaskList.svelte`, wrap the read of `sortableActiveTasks` inside the `$effect` with `untrack()` (import from `svelte`) to prevent the effect from re-running when it writes to `sortableActiveTasks`
- [x] 3.2 Verify that task completion animation still works (the `justCompleted` detection) after the `untrack()` change

## 4. Scope Click-Outside Handlers

- [x] 4.1 ~~Scope SearchBar click-outside handler~~ — Reverted: conditional document listener caused test timing issues. Kept original `<svelte:window onclick>` approach.
- [x] 4.2 ~~Scope ExportButton click-outside handler~~ — Reverted: same reasoning as 4.1.

## 5. Verification

- [x] 5.1 Run `cd frontend && npm run check` to verify no type errors — 0 errors, 4 pre-existing warnings
- [x] 5.2 Run the full E2E test suite (`uv run python -m pytest e2e -q`) and confirm no regressions — 82 passed, 1 flaky (pre-existing search timing), 5 pre-existing network_links errors
- [x] 5.3 Run the new navigation E2E test and confirm it passes
