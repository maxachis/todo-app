## 1. Deferred Task Removal

- [x] 1.1 Update `frontend/src/lib/components/tasks/TaskList.svelte` — modify the `$effect` that builds `sortableActiveTasks` to detect newly-completed tasks and delay their removal by 300ms, keeping them visible with `.completed` styling during the transition
- [x] 1.2 Ensure the `setTimeout` cleanup is handled properly — store the timeout ID and clear it if the effect re-runs before the timeout fires (prevents stale removals)

## 2. Verification

- [x] 2.1 Run `cd frontend && npm run check` to verify TypeScript compiles with no errors
- [ ] 2.2 Manually test completing a task at the bottom of a long list — confirm no black flash
- [ ] 2.3 Manually test rapid successive completions — confirm no visual glitches
- [ ] 2.4 Manually test dragging a task while another is in its 300ms fade-out — confirm DnD still works
