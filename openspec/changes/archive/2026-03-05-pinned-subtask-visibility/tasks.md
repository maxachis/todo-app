## 1. Recursive Pinned Task Collection

- [x] 1.1 Add a `collectPinnedTasks` helper function in `frontend/src/routes/+page.svelte` that recursively walks the task tree and returns `{ task: Task, parentTitle: string }[]` for all pinned, non-completed tasks
- [x] 1.2 Update the `pinnedTasks` derived to use `collectPinnedTasks` instead of the flat `flatMap` + `filter`

## 2. PinnedSection Component Update

- [x] 2.1 Update `PinnedSection.svelte` props to accept `{ task: Task, parentTitle: string }[]` instead of `Task[]`
- [x] 2.2 Render parent context prefix (dimmed "Parent >" before the task title) when `parentTitle` is non-empty
- [x] 2.3 Style the parent prefix with secondary text color and separator

## 3. Wire Up and Verify

- [x] 3.1 Update PinnedSection usage in `+page.svelte` to pass the new shape and adapt `onReorder` callback
- [x] 3.2 Run `npm run check` in `frontend/` to verify no type errors
