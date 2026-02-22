## 1. Sort State and Logic

- [x] 1.1 Add `$state` variables for `sortField` (default `'last_name'`) and `sortDirection` (default `'asc'`) in `frontend/src/routes/people/+page.svelte`
- [x] 1.2 Add a `$derived` `sortedPeople` array that sorts `people` by the active field and direction, with null `follow_up_cadence_days` pushed to the end when sorting by that field
- [x] 1.3 Replace the `{#each people ...}` loop with `{#each sortedPeople ...}` so the list renders from the derived sorted array
- [x] 1.4 Remove the hardcoded `.sort()` call in `createPerson` — just append the new person to `people` and let `sortedPeople` handle ordering

## 2. Sort Control UI

- [x] 2.1 Add a sort bar between the create form and the list in `frontend/src/routes/people/+page.svelte` containing a `<select>` with options Last Name / First Name / Follow Up Days and a direction toggle button showing an arrow indicator
- [x] 2.2 Bind the `<select>` to `sortField` and the toggle button to flip `sortDirection` between `'asc'` and `'desc'`
- [x] 2.3 Style the sort bar to match the existing panel aesthetic (compact, inline layout, using existing CSS variables from `+page.svelte`)

## 3. Verification

- [x] 3.1 Manually verify: page loads with Last Name ascending (matches previous behavior), switching fields and toggling direction re-sorts the list, creating a new person inserts in the correct sorted position
- [x] 3.2 Verify null follow-up cadence people sort to the end in both ascending and descending Follow Up Days sort
- [x] 3.3 Run `cd frontend && npm run check` to confirm no type or lint errors
