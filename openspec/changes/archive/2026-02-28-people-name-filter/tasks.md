## 1. Add filter state and reactive pipeline

- [x] 1.1 Add `filterQuery` `$state('')` variable to `frontend/src/routes/people/+page.svelte`
- [x] 1.2 Update the `$derived.by()` block: filter `people` array by case-insensitive substring match on `first_name` and `last_name` before sorting, rename result to `filteredAndSortedPeople`
- [x] 1.3 Update the `{#each}` block to iterate over `filteredAndSortedPeople` instead of `sortedPeople`

## 2. Add filter input to the sort bar

- [x] 2.1 Add a text `<input>` to the `.sort-bar` div in `frontend/src/routes/people/+page.svelte`, bound to `filterQuery`, with placeholder text (e.g. "Filter by name...")
- [x] 2.2 Style the input to fit alongside the existing sort selector and direction toggle, including responsive behavior for the single-column layout

## 3. Verify

- [ ] 3.1 Manual verification: filter narrows list, composes with sort, persists on person selection, clearing restores full list
