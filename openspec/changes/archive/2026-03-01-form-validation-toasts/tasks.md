## 1. Shared Validation Helper

- [x] 1.1 Create `frontend/src/lib/utils/validation.ts` with `validateRequired` function that accepts `Record<string, string | number | null | undefined | unknown[]>`, checks for empty/null/zero-length values, calls `addToast({ message: 'Required: ...', type: 'error' })` for failures, and returns boolean
- [x] 1.2 Verify helper handles all value types: empty string, whitespace-only string, `null`, `undefined`, empty array, and valid values

## 2. CRM Form Integration

- [x] 2.1 Update `frontend/src/routes/crm/people/+page.svelte` — `createPerson`: replace `if (!newFirst.trim() || !newLast.trim()) return;` with `validateRequired({ 'First name': newFirst, 'Last name': newLast })`
- [x] 2.2 Update `frontend/src/routes/crm/people/+page.svelte` — quick-log interaction: replace `if (!selected || !quickLogTypeId || !quickLogDate) return;` with validateRequired check for Type and Date (keep the `!selected` guard separate since it's not a user-facing validation)
- [x] 2.3 Update `frontend/src/routes/crm/orgs/+page.svelte` — `createOrganization`: replace `if (!newOrgName.trim() || !newOrgTypeId) return;` with `validateRequired({ 'Name': newOrgName, 'Organization type': newOrgTypeId })`
- [x] 2.4 Update `frontend/src/routes/crm/interactions/+page.svelte` — `createInteraction`: replace `if (newPersonIds.length === 0 || !newTypeId || !newDate) return;` with `validateRequired({ 'People': newPersonIds, 'Type': newTypeId, 'Date': newDate })`
- [x] 2.5 Update `frontend/src/routes/crm/leads/+page.svelte` — `createLead`: replace silent checks with `validateRequired({ 'Title': newTitle })` and a separate check for person-or-org with a descriptive toast

## 3. Network Form Integration

- [x] 3.1 Update `frontend/src/routes/network/relationships/+page.svelte` — person-person create: replace `if (!newPerson1Id || newPersonBIds.length === 0) return;` with `validateRequired({ 'Person A': newPerson1Id, 'Person B': newPersonBIds })`
- [x] 3.2 Update `frontend/src/routes/network/relationships/+page.svelte` — org-person create: replace `if (!newOrgId || newOrgPersonIds.length === 0) return;` with `validateRequired({ 'Organization': newOrgId, 'People': newOrgPersonIds })`

## 4. Project & Timesheet Form Integration

- [x] 4.1 Update `frontend/src/routes/projects/+page.svelte` — `createProject`: replace `if (!newName.trim()) return;` with `validateRequired({ 'Name': newName })`
- [x] 4.2 Update `frontend/src/routes/projects/+page.svelte` — add project link: replace `if (!newLinkDescriptor.trim() || !newLinkUrl.trim()) return;` with `validateRequired({ 'Label': newLinkDescriptor, 'URL': newLinkUrl })`
- [x] 4.3 Update `frontend/src/routes/timesheet/+page.svelte` — `handleCreate`: replace `if (newProjectId === null) return;` with `validateRequired({ 'Project': newProjectId })`

## 5. Task & List Form Integration

- [x] 5.1 Update `frontend/src/lib/components/tasks/TaskCreateForm.svelte` — replace silent trim check with `validateRequired({ 'Title': title })` (or equivalent variable name)
- [x] 5.2 Update `frontend/src/lib/components/lists/ListSidebar.svelte` — replace silent trim check on list creation with `validateRequired({ 'Name': newListName })`

## 6. Verification

- [x] 6.1 Run `cd frontend && npm run check` to verify TypeScript compiles with no errors
- [ ] 6.2 Manually test each form by submitting empty — confirm error toast appears with correct field names
- [ ] 6.3 Manually test each form with all fields filled — confirm normal submit still works
