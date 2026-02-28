## 1. Filter State and Derived Computations

- [x] 1.1 Add `filterPersonId` and `filterOrgId` state variables to `frontend/src/routes/relationships/+page.svelte`
- [x] 1.2 Add `$derived` computed `filteredPersonRelationships` that filters `personRelationships` by `filterPersonId` (checking both `person_1_id` and `person_2_id`), falling back to the full list when null
- [x] 1.3 Add `$derived` computed `filteredOrgRelationships` that filters `orgRelationships` by `filterOrgId` (checking `organization_id`), falling back to the full list when null

## 2. Auto-Sync From Form to Filter

- [x] 2.1 Add `$effect` that sets `filterPersonId` whenever `newPerson1Id` changes (including clearing to null)
- [x] 2.2 Add `$effect` that sets `filterOrgId` whenever `newOrgId` changes (including clearing to null)

## 3. Exclude Existing Connections from Secondary Dropdowns

- [x] 3.1 Add `$derived` computed `availablePersonBOptions` that excludes Person A and all people already connected to Person A from the Person B TypeaheadSelect options
- [x] 3.2 Add `$derived` computed `availableOrgPersonOptions` that excludes people already linked to the selected Organization from the Person TypeaheadSelect options
- [x] 3.3 Update Person B TypeaheadSelect `options` prop to use `availablePersonBOptions` instead of the full people list
- [x] 3.4 Update org-person Person TypeaheadSelect `options` prop to use `availableOrgPersonOptions` instead of the full people list

## 4. Filter UI Controls

- [x] 4.1 Add a filter TypeaheadSelect (with × clear button) between the create form and the relationship list in the Person ↔ Person panel, bound to `filterPersonId`, populated with all people
- [x] 4.2 Add a filter TypeaheadSelect (with × clear button) between the create form and the relationship list in the Organization → Person panel, bound to `filterOrgId`, populated with all organizations
- [x] 4.3 Style the filter row (inline layout with clear button, visual separator from form and list)

## 5. Wire Filtered Lists to Rendering

- [x] 5.1 Update the `{#each}` loop in the Person ↔ Person panel to iterate over `filteredPersonRelationships` instead of `personRelationships`
- [x] 5.2 Update the `{#each}` loop in the Organization → Person panel to iterate over `filteredOrgRelationships` instead of `orgRelationships`

## 6. Verification

- [x] 6.1 Verify: selecting Person A auto-filters the list and excludes connected people from Person B dropdown
- [x] 6.2 Verify: selecting Organization auto-filters the list and excludes linked people from Person dropdown
- [x] 6.3 Verify: submitting a relationship clears the filter and updates both the list and dropdown exclusions
- [x] 6.4 Verify: filter can be changed independently without affecting the create form
- [x] 6.5 Verify: clearing the filter (× button) shows all relationships
- [x] 6.6 Run `cd frontend && npm run check` to verify no type errors
