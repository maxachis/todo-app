## Why

The unified app has Svelte pages for People, Organizations, Interactions, Relationships, and Graph, but they are unreachable — the navbar and mobile tab bar only link to Tasks, Upcoming, Projects, Timesheet, and Import. Additionally, the bridge models and API endpoints for linking tasks to network entities (TaskPerson, TaskOrganization, InteractionTask) exist but have no frontend UI. Users cannot navigate to network pages or see which people/organizations relate to a task.

## What Changes

- Add People, Organizations, Interactions, Relationships, and Graph entries to the top navbar and mobile tab bar in `+layout.svelte`.
- Add a "Linked People & Organizations" section to the task detail panel, allowing users to view, add, and remove linked network entities on any task.
- Add a "Linked Tasks" section to the person, organization, and interaction detail panels, showing tasks associated with each entity and allowing link/unlink.
- Add frontend API methods and TypeScript types for the existing task-link endpoints (`/api/tasks/:id/people/`, `/api/tasks/:id/organizations/`, `/api/interactions/:id/tasks/`).

## Capabilities

### New Capabilities
- `task-link-ui`: Svelte components and page integrations for displaying and managing links between tasks and network entities (people, organizations, interactions) on both the task detail panel and network detail pages.

### Modified Capabilities
- `svelte-frontend`: The top navigation bar and mobile tab bar gain entries for all network pages. The task detail panel gains a new section for linked network entities.
- `network-frontend`: Person, organization, and interaction detail views gain linked-tasks sections.

## Impact

- Frontend: Updated `+layout.svelte` navigation, new Svelte components for link display/management, changes to TaskDetail.svelte and the people/organizations/interactions page components.
- API client: New methods in `frontend/src/lib/api/index.ts` for task-link endpoints (endpoints already exist in backend).
- No backend changes required — all API endpoints and models are already in place.

## Non-goals

- No changes to the network page CRUD functionality (create/edit/delete people, orgs, interactions already works).
- No changes to the graph visualization page.
- No backend API or model changes.
