## ADDED Requirements

### Requirement: Lead entity with title, status, and contact associations
The system SHALL provide a Lead model with a `title` (CharField, max 255), `status` (CharField with choices: prospect, interested, committed, fulfilled, unfulfilled, default prospect), `notes` (TextField, blank), optional `person` FK (SET_NULL), and optional `organization` FK (SET_NULL). A database CheckConstraint SHALL enforce that at least one of person or organization is not null. The model SHALL include `created_at` and `updated_at` timestamps.

#### Scenario: Create lead with person only
- **WHEN** a lead is created with a title, status, and person but no organization
- **THEN** the lead is persisted with the person association and organization as null

#### Scenario: Create lead with organization only
- **WHEN** a lead is created with a title, status, and organization but no person
- **THEN** the lead is persisted with the organization association and person as null

#### Scenario: Create lead with both person and organization
- **WHEN** a lead is created with both a person and an organization
- **THEN** both associations are persisted on the lead

#### Scenario: Reject lead with neither person nor organization
- **WHEN** a lead creation is attempted with both person and organization as null
- **THEN** the system SHALL reject the request with a validation error

### Requirement: Lead status values
The Lead status field SHALL accept exactly these values: prospect, interested, committed, fulfilled, unfulfilled. The default status for new leads SHALL be "prospect".

#### Scenario: Create lead with default status
- **WHEN** a lead is created without specifying a status
- **THEN** the lead status is set to "prospect"

#### Scenario: Update lead status
- **WHEN** a lead's status is changed from "prospect" to "committed"
- **THEN** the new status is persisted and updated_at changes

### Requirement: Lead-task link table
The system SHALL provide a LeadTask link model with a `lead` FK (CASCADE) and a `task` FK (CASCADE), a unique constraint on the (lead, task) pair, and a `created_at` timestamp. Deleting a lead SHALL cascade-delete its task links. Deleting a task SHALL cascade-delete its lead links.

#### Scenario: Link task to lead
- **WHEN** a task is linked to a lead
- **THEN** the association is persisted and retrievable from both the lead and task context

#### Scenario: Prevent duplicate lead-task link
- **WHEN** a link between the same lead and task already exists
- **THEN** the system SHALL not create a duplicate link

#### Scenario: Delete lead cascades to links
- **WHEN** a lead with linked tasks is deleted
- **THEN** all LeadTask links for that lead are also deleted

### Requirement: Leads CRUD API
The system SHALL expose Django Ninja API endpoints for leads: GET /api/leads/ (list, ordered by -updated_at), POST /api/leads/ (create, returns 201), GET /api/leads/{id}/ (detail), PUT /api/leads/{id}/ (update), DELETE /api/leads/{id}/ (returns 204). The list and detail endpoints SHALL include the associated person name and organization name.

#### Scenario: List leads
- **WHEN** GET /api/leads/ is called
- **THEN** all leads are returned ordered by most recently updated first, each including person_name and organization_name

#### Scenario: Create lead via API
- **WHEN** POST /api/leads/ is called with valid title and person_id
- **THEN** the lead is created and returned with status 201

#### Scenario: Update lead via API
- **WHEN** PUT /api/leads/{id}/ is called with a new title
- **THEN** only the title is updated; other fields remain unchanged

#### Scenario: Delete lead via API
- **WHEN** DELETE /api/leads/{id}/ is called
- **THEN** the lead and its task links are deleted, returning status 204

### Requirement: Lead-task link API
The system SHALL expose endpoints for lead-task links: GET /api/leads/{lead_id}/tasks/ (list linked tasks), POST /api/leads/{lead_id}/tasks/ (link a task, returns 201 if new or 200 if existing), DELETE /api/leads/{lead_id}/tasks/{task_id}/ (unlink, returns 204).

#### Scenario: List tasks linked to a lead
- **WHEN** GET /api/leads/{lead_id}/tasks/ is called
- **THEN** all task IDs linked to the lead are returned

#### Scenario: Link task to lead via API
- **WHEN** POST /api/leads/{lead_id}/tasks/ is called with a task_id
- **THEN** the link is created (or returned if already existing)

#### Scenario: Unlink task from lead via API
- **WHEN** DELETE /api/leads/{lead_id}/tasks/{task_id}/ is called
- **THEN** the link is removed and status 204 is returned

### Requirement: Leads page with two-panel list and detail layout
The frontend SHALL provide a /leads route with a two-panel layout: a left list panel showing all leads with title, person/org name, and status badge, and a right detail panel showing the selected lead's editable fields (title, status, person, organization, notes) and linked tasks.

#### Scenario: View leads list
- **WHEN** the user navigates to /leads
- **THEN** all leads are displayed in a scrollable list with title, associated contact name, and status badge

#### Scenario: Select lead to view detail
- **WHEN** the user clicks a lead in the list
- **THEN** the detail panel shows the lead's title, status selector, person/org fields, notes, and linked tasks

#### Scenario: Create new lead from list panel
- **WHEN** the user enters a title in the creation form and submits
- **THEN** a new lead is created with default status "prospect" and appears in the list

#### Scenario: Edit lead fields in detail panel
- **WHEN** the user modifies a lead's title, status, notes, person, or organization in the detail panel
- **THEN** the changes are saved via API on blur and the list reflects the update

#### Scenario: Link and unlink tasks in detail panel
- **WHEN** the user adds or removes a task link in the lead detail panel
- **THEN** the link is persisted via API and the linked tasks list updates

### Requirement: Leads nav tab
The frontend layout SHALL include a "Leads" tab in the top navigation bar, placed after Graph and before Projects, linking to the /leads route.

#### Scenario: Navigate to leads via nav tab
- **WHEN** the user clicks the "Leads" tab in the navigation bar
- **THEN** the app navigates to the /leads page
