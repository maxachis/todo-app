## 1. Replace tag input with TypeaheadSelect

- [x] 1.1 In `frontend/src/lib/components/tasks/TaskDetail.svelte`, import `TypeaheadSelect` from `$lib/components/shared/TypeaheadSelect.svelte`
- [x] 1.2 Replace the `<form class="tag-form">` block (input + datalist + "+" button) with a `<TypeaheadSelect>` component in action mode: pass `options` mapped from `availableTags` (`{id, label}` format), `placeholder="Add tag..."`, `onSelect` callback, and `onCreate` callback
- [x] 1.3 Remove the `tagInput` state variable and the `addTag(event: SubmitEvent)` function that handled form submission

## 2. Wire up onSelect and onCreate callbacks

- [x] 2.1 Implement the `onSelect` callback: given a tag id, call `api.tasks.addTag(task.id, tagName)` where tagName is resolved from `availableTags`, then call `refreshTask(task.id)` and `loadAvailableTags(task.id)` to update both the task display and the dropdown options
- [x] 2.2 Implement the `onCreate` callback: given a new tag name string, call `api.tasks.addTag(task.id, name)` (the backend auto-creates tags), refresh the task and available tags, and return `{id, label}` for the newly created tag

## 3. Verify and test

- [x] 3.1 Verify the tag field renders TypeaheadSelect with correct options and that selecting a tag adds it immediately without a submit button
- [x] 3.2 Verify creating a new tag via the "Create …" option works end-to-end
- [x] 3.3 Verify the available tags list updates after each add (the added tag no longer appears in suggestions)
