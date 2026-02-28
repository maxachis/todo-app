## 1. Add filter state and reactive filtering

- [x] 1.1 Add `filterQuery` `$state('')` variable to `frontend/src/routes/organizations/+page.svelte`
- [x] 1.2 Add a `filteredOrganizations` `$derived` that filters `organizations` by case-insensitive substring match on `name`
- [x] 1.3 Update the `{#each}` block to iterate over `filteredOrganizations` instead of `organizations`

## 2. Add filter input to the UI

- [x] 2.1 Add a text `<input>` between the `.create-form` and `.list` divs, bound to `filterQuery`, with placeholder text (e.g. "Filter by name…")
- [x] 2.2 Style the filter input consistently with the People page filter

## 3. Verify

- [ ] 3.1 Manual verification: filter narrows list, persists on org selection, clearing restores full list
