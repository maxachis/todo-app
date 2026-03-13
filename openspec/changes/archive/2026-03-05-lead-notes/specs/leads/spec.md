## MODIFIED Requirements

### Requirement: Leads page with two-panel list and detail layout
The frontend SHALL provide a /leads route with a two-panel layout: a left list panel showing all leads with title, person/org name, and status badge, and a right detail panel showing the selected lead's editable fields (title, status, person, organization, notes) and linked tasks. The creation form in the list panel SHALL include a notes textarea.

#### Scenario: View leads list
- **WHEN** the user navigates to /leads
- **THEN** all leads are displayed in a scrollable list with title, associated contact name, and status badge

#### Scenario: Select lead to view detail
- **WHEN** the user clicks a lead in the list
- **THEN** the detail panel shows the lead's title, status selector, person/org fields, notes, and linked tasks

#### Scenario: Create new lead from list panel
- **WHEN** the user enters a title, optionally fills in notes, and submits the creation form
- **THEN** a new lead is created with the provided notes (or empty string if omitted), default status "prospect", and appears in the list

#### Scenario: Create new lead with notes
- **WHEN** the user fills in title, notes, and a person/org, then submits
- **THEN** the lead is created with the notes persisted and both title and notes fields are cleared

#### Scenario: Edit lead fields in detail panel
- **WHEN** the user modifies a lead's title, status, notes, person, or organization in the detail panel
- **THEN** the changes are saved via API on blur and the list reflects the update

#### Scenario: Link and unlink tasks in detail panel
- **WHEN** the user adds or removes a task link in the lead detail panel
- **THEN** the link is persisted via API and the linked tasks list updates
