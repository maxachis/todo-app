## 1. Navigation Updates

- [x] 1.1 Add People, Organizations, Interactions, Relationships, and Graph entries to the `tabs` array in `frontend/src/routes/+layout.svelte` with hrefs `/people`, `/organizations`, `/interactions`, `/relationships`, `/graph`
- [x] 1.2 Make the mobile bottom tab bar horizontally scrollable (`overflow-x: auto`) to accommodate 10 tabs
- [x] 1.3 Update `grid-template-columns` on `.mobile-tabs` from `repeat(4, 1fr)` to `repeat(10, auto)` (or remove fixed columns) so all tabs fit

## 2. TypeScript Types

- [x] 2.1 Add `TaskPersonLink` interface (`id`, `task_id`, `person_id`, `created_at`) to `frontend/src/lib/api/types.ts`
- [x] 2.2 Add `TaskOrganizationLink` interface (`id`, `task_id`, `organization_id`, `created_at`) to `frontend/src/lib/api/types.ts`
- [x] 2.3 Add `InteractionTaskLink` interface (`id`, `interaction_id`, `task_id`, `created_at`) to `frontend/src/lib/api/types.ts`

## 3. API Client Methods

- [x] 3.1 Add `taskLinks.people.list(taskId)` → `GET /api/tasks/{taskId}/people/` to `frontend/src/lib/api/index.ts`
- [x] 3.2 Add `taskLinks.people.add(taskId, personId)` → `POST /api/tasks/{taskId}/people/` with body `{ id: personId }` to `frontend/src/lib/api/index.ts`
- [x] 3.3 Add `taskLinks.people.remove(taskId, personId)` → `DELETE /api/tasks/{taskId}/people/{personId}/` to `frontend/src/lib/api/index.ts`
- [x] 3.4 Add `taskLinks.organizations.list(taskId)` → `GET /api/tasks/{taskId}/organizations/` to `frontend/src/lib/api/index.ts`
- [x] 3.5 Add `taskLinks.organizations.add(taskId, organizationId)` → `POST /api/tasks/{taskId}/organizations/` with body `{ id: organizationId }` to `frontend/src/lib/api/index.ts`
- [x] 3.6 Add `taskLinks.organizations.remove(taskId, organizationId)` → `DELETE /api/tasks/{taskId}/organizations/{organizationId}/` to `frontend/src/lib/api/index.ts`
- [x] 3.7 Add `taskLinks.interactions.list(interactionId)` → `GET /api/interactions/{interactionId}/tasks/` to `frontend/src/lib/api/index.ts`
- [x] 3.8 Add `taskLinks.interactions.add(interactionId, taskId)` → `POST /api/interactions/{interactionId}/tasks/` with body `{ id: taskId }` to `frontend/src/lib/api/index.ts`
- [x] 3.9 Add `taskLinks.interactions.remove(interactionId, taskId)` → `DELETE /api/interactions/{interactionId}/tasks/{taskId}/` to `frontend/src/lib/api/index.ts`

## 4. Shared LinkedEntities Component

- [x] 4.1 Create `frontend/src/lib/components/shared/LinkedEntities.svelte` — a reusable component that accepts: entity list, linked IDs, display name resolver function, add callback, and remove callback. Renders a list of linked entity names with remove buttons and a `<select>` dropdown to add new links (excluding already-linked entities).

## 5. Task Detail — Linked People & Orgs

- [x] 5.1 In `frontend/src/lib/components/tasks/TaskDetail.svelte`, add a "Linked People & Orgs" section below the tags section
- [x] 5.2 On task selection, fetch linked people via `api.taskLinks.people.list(taskId)` and linked organizations via `api.taskLinks.organizations.list(taskId)`
- [x] 5.3 Fetch the full people list (`api.people.getAll()`) and organizations list (`api.organizations.getAll()`) for name resolution and dropdown population
- [x] 5.4 Wire the `LinkedEntities` component for people: display linked person names, add via dropdown, remove via button
- [x] 5.5 Wire the `LinkedEntities` component for organizations: display linked org names, add via dropdown, remove via button
- [x] 5.6 Show "No linked people or organizations" placeholder when both link lists are empty

## 6. Network Pages — Linked Tasks

- [x] 6.1 In `frontend/src/routes/people/+page.svelte`, add a "Linked Tasks" section to the person detail area using the `LinkedEntities` component. Fetch linked tasks by iterating task-person links for the selected person. Provide a task dropdown for adding and a remove button for unlinking.
- [x] 6.2 In `frontend/src/routes/organizations/+page.svelte`, add a "Linked Tasks" section to the organization detail area using the same pattern as 6.1 but for task-organization links.
- [x] 6.3 In `frontend/src/routes/interactions/+page.svelte`, add a "Linked Tasks" section to the interaction detail area using `api.taskLinks.interactions` methods.

## 7. Frontend Type Check

- [x] 7.1 Run `cd frontend && npm run check` and fix any TypeScript errors introduced by the changes

## 8. E2E Tests

- [x] 8.1 Add E2E test: verify all 10 navigation tabs are visible and link to the correct routes
- [x] 8.2 Add E2E test: select a task, link a person via the detail panel dropdown, verify the person appears in the linked list, then unlink and verify removal
- [x] 8.3 Add E2E test: navigate to People page, select a person, link a task from the detail panel, verify it appears, then unlink
