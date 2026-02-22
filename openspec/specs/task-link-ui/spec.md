### Requirement: TypeScript types for task-entity links
The system SHALL define TypeScript interfaces for the task-person, task-organization, and interaction-task link objects returned by the API.

#### Scenario: TaskPersonLink type
- **WHEN** the frontend TypeScript types are defined
- **THEN** a `TaskPersonLink` interface exists with fields `id: number`, `task_id: number`, `person_id: number`, `created_at: string`

#### Scenario: TaskOrganizationLink type
- **WHEN** the frontend TypeScript types are defined
- **THEN** a `TaskOrganizationLink` interface exists with fields `id: number`, `task_id: number`, `organization_id: number`, `created_at: string`

#### Scenario: InteractionTaskLink type
- **WHEN** the frontend TypeScript types are defined
- **THEN** an `InteractionTaskLink` interface exists with fields `id: number`, `interaction_id: number`, `task_id: number`, `created_at: string`

### Requirement: API client methods for task-person links
The system SHALL provide typed API client methods for listing, creating, and removing links between tasks and people.

#### Scenario: List people linked to a task
- **WHEN** the client calls `api.taskLinks.people.list(taskId)`
- **THEN** a GET request is sent to `/api/tasks/{taskId}/people/` and the response is typed as `TaskPersonLink[]`

#### Scenario: Link a person to a task
- **WHEN** the client calls `api.taskLinks.people.add(taskId, personId)`
- **THEN** a POST request is sent to `/api/tasks/{taskId}/people/` with body `{ id: personId }` and the response is typed as `TaskPersonLink`

#### Scenario: Unlink a person from a task
- **WHEN** the client calls `api.taskLinks.people.remove(taskId, personId)`
- **THEN** a DELETE request is sent to `/api/tasks/{taskId}/people/{personId}/`

### Requirement: API client methods for task-organization links
The system SHALL provide typed API client methods for listing, creating, and removing links between tasks and organizations.

#### Scenario: List organizations linked to a task
- **WHEN** the client calls `api.taskLinks.organizations.list(taskId)`
- **THEN** a GET request is sent to `/api/tasks/{taskId}/organizations/` and the response is typed as `TaskOrganizationLink[]`

#### Scenario: Link an organization to a task
- **WHEN** the client calls `api.taskLinks.organizations.add(taskId, organizationId)`
- **THEN** a POST request is sent to `/api/tasks/{taskId}/organizations/` with body `{ id: organizationId }` and the response is typed as `TaskOrganizationLink`

#### Scenario: Unlink an organization from a task
- **WHEN** the client calls `api.taskLinks.organizations.remove(taskId, organizationId)`
- **THEN** a DELETE request is sent to `/api/tasks/{taskId}/organizations/{organizationId}/`

### Requirement: API client methods for interaction-task links
The system SHALL provide typed API client methods for listing, creating, and removing links between interactions and tasks.

#### Scenario: List tasks linked to an interaction
- **WHEN** the client calls `api.taskLinks.interactions.list(interactionId)`
- **THEN** a GET request is sent to `/api/interactions/{interactionId}/tasks/` and the response is typed as `InteractionTaskLink[]`

#### Scenario: Link a task to an interaction
- **WHEN** the client calls `api.taskLinks.interactions.add(interactionId, taskId)`
- **THEN** a POST request is sent to `/api/interactions/{interactionId}/tasks/` with body `{ id: taskId }` and the response is typed as `InteractionTaskLink`

#### Scenario: Unlink a task from an interaction
- **WHEN** the client calls `api.taskLinks.interactions.remove(interactionId, taskId)`
- **THEN** a DELETE request is sent to `/api/interactions/{interactionId}/tasks/{taskId}/`

### Requirement: Linked people and organizations section in task detail
The system SHALL display a "Linked People & Orgs" section in the task detail panel showing all people and organizations linked to the selected task, with controls to add and remove links.

#### Scenario: Section displays linked people
- **WHEN** a task is selected and has linked people
- **THEN** the task detail panel shows a "Linked People & Orgs" section listing each linked person by full name

#### Scenario: Section displays linked organizations
- **WHEN** a task is selected and has linked organizations
- **THEN** the "Linked People & Orgs" section also lists each linked organization by name

#### Scenario: Empty state when no links exist
- **WHEN** a task is selected and has no linked people or organizations
- **THEN** the section shows placeholder text such as "No linked people or organizations"

#### Scenario: Add a person link via typeahead
- **WHEN** the user types into the add-person typeahead input and selects a person from the filtered results
- **THEN** the person is linked to the task via the API, appears in the list immediately, and the typeahead input clears

#### Scenario: Add an organization link via typeahead
- **WHEN** the user types into the add-organization typeahead input and selects an organization from the filtered results
- **THEN** the organization is linked to the task via the API, appears in the list immediately, and the typeahead input clears

#### Scenario: Remove a person link
- **WHEN** the user clicks the remove button next to a linked person
- **THEN** the link is removed via the API and the person disappears from the list immediately

#### Scenario: Remove an organization link
- **WHEN** the user clicks the remove button next to a linked organization
- **THEN** the link is removed via the API and the organization disappears from the list immediately

#### Scenario: Typeahead excludes already-linked entities
- **WHEN** the user focuses the add-person or add-organization typeahead input
- **THEN** entities already linked to the task are excluded from the typeahead options

#### Scenario: Links load when task is selected
- **WHEN** the user selects a task in the center panel
- **THEN** the linked people and organizations are fetched from the API and displayed in the detail panel

### Requirement: Linked tasks section in network detail views
The system SHALL display a "Linked Tasks" section in the person, organization, and interaction detail views, showing tasks associated with each entity and allowing link/unlink.

#### Scenario: Person detail shows linked tasks
- **WHEN** a person is selected in the People page
- **THEN** the detail panel shows a "Linked Tasks" section listing tasks linked to that person, with each task showing its title

#### Scenario: Organization detail shows linked tasks
- **WHEN** an organization is selected in the Organizations page
- **THEN** the detail panel shows a "Linked Tasks" section listing tasks linked to that organization

#### Scenario: Interaction detail shows linked tasks
- **WHEN** an interaction is selected in the Interactions page
- **THEN** the detail panel shows a "Linked Tasks" section listing tasks linked to that interaction

#### Scenario: Add a task link from person detail
- **WHEN** the user clicks the add button in the linked tasks section of a person detail and selects a task
- **THEN** the task is linked to the person via the API and appears in the list

#### Scenario: Remove a task link from person detail
- **WHEN** the user clicks the remove button next to a linked task in a person detail
- **THEN** the link is removed via the API and the task disappears from the list

#### Scenario: Add a task link from interaction detail
- **WHEN** the user clicks the add button in the linked tasks section of an interaction detail and selects a task
- **THEN** the task is linked to the interaction via `POST /api/interactions/{id}/tasks/` and appears in the list

#### Scenario: Linked tasks empty state
- **WHEN** a person, organization, or interaction has no linked tasks
- **THEN** the section shows placeholder text such as "No linked tasks"
