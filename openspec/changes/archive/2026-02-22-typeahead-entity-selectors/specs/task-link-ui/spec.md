## MODIFIED Requirements

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
