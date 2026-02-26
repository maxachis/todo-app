### Requirement: Project link data model
The system SHALL store project links as a separate entity with a foreign key to Project. Each link SHALL have a `url` (max 2000 chars, required) and a `descriptor` (max 100 chars, required). Links SHALL be deleted when their parent project is deleted (CASCADE).

#### Scenario: Create a project link record
- **WHEN** a project link is created with url "https://github.com/org/repo" and descriptor "GitHub Repo"
- **THEN** the link is persisted with the given url, descriptor, project foreign key, and an auto-generated created_at timestamp

#### Scenario: Delete parent project cascades to links
- **WHEN** a project that has associated links is deleted
- **THEN** all of its links are also deleted

### Requirement: List project links
The system SHALL provide an endpoint `GET /projects/{project_id}/links/` that returns all links for the given project, ordered by creation time ascending.

#### Scenario: List links for a project with links
- **WHEN** a GET request is made to `/projects/{project_id}/links/` for a project with 3 links
- **THEN** the response contains all 3 links with id, url, descriptor, project_id, and created_at fields

#### Scenario: List links for a project with no links
- **WHEN** a GET request is made to `/projects/{project_id}/links/` for a project with no links
- **THEN** the response is an empty array

### Requirement: Create project link
The system SHALL provide an endpoint `POST /projects/{project_id}/links/` that creates a new link for the given project. Both `url` and `descriptor` fields are required and SHALL be stripped of leading/trailing whitespace. The endpoint SHALL return 201 on success.

#### Scenario: Successfully create a link
- **WHEN** a POST request is made with url "https://figma.com/file/abc" and descriptor "Mockups"
- **THEN** the system creates the link, returns 201 with the serialized link including its generated id

#### Scenario: Create with blank url
- **WHEN** a POST request is made with url "" (empty) and descriptor "Something"
- **THEN** the system returns 422 with an error message

#### Scenario: Create with blank descriptor
- **WHEN** a POST request is made with url "https://example.com" and descriptor "" (empty)
- **THEN** the system returns 422 with an error message

### Requirement: Update project link
The system SHALL provide an endpoint `PUT /projects/{project_id}/links/{link_id}/` that updates an existing link's url and/or descriptor. Fields are optional; only provided fields are updated. Values SHALL be stripped of whitespace.

#### Scenario: Update link descriptor
- **WHEN** a PUT request is made with descriptor "Production App" for an existing link
- **THEN** the link's descriptor is updated and the full link is returned

#### Scenario: Update link url
- **WHEN** a PUT request is made with url "https://new-url.com" for an existing link
- **THEN** the link's url is updated and the full link is returned

#### Scenario: Update with blank url
- **WHEN** a PUT request is made with url "" (empty string)
- **THEN** the system returns 422 with an error message

### Requirement: Delete project link
The system SHALL provide an endpoint `DELETE /projects/{project_id}/links/{link_id}/` that removes the link. Returns 204 on success.

#### Scenario: Successfully delete a link
- **WHEN** a DELETE request is made for an existing link
- **THEN** the link is removed and 204 is returned

#### Scenario: Delete non-existent link
- **WHEN** a DELETE request is made for a link id that does not exist
- **THEN** the system returns 404

### Requirement: Links included in project list response
The system SHALL include a `links` array in the project list/detail response schema, containing all links for each project. Links SHALL be eagerly loaded to avoid N+1 queries.

#### Scenario: Project response includes links
- **WHEN** projects are fetched via `GET /projects/`
- **THEN** each project object includes a `links` array with all its associated links (id, url, descriptor, project_id, created_at)

#### Scenario: Project with no links
- **WHEN** a project with no links is fetched
- **THEN** the project's `links` array is empty

### Requirement: Frontend displays project links on card
The system SHALL display project links on the project card as a list of clickable anchors. Each link SHALL show the descriptor as the anchor text and open the url in a new tab.

#### Scenario: View links on a project card
- **WHEN** a project with links is displayed
- **THEN** each link appears as a clickable anchor with the descriptor as text, opening the url in a new tab with rel="noopener noreferrer"

#### Scenario: Project card with no links
- **WHEN** a project with no links is displayed
- **THEN** no links section is shown on the card

### Requirement: Frontend add link inline
The system SHALL provide an inline form on the project card to add a new link with descriptor and url inputs. The form SHALL appear when an "Add link" button is clicked and SHALL submit via the API.

#### Scenario: Add a link via inline form
- **WHEN** the user clicks "Add link", fills in descriptor "Docs" and url "https://docs.example.com", and submits
- **THEN** the link is created via the API and appears in the links list on the card

### Requirement: Frontend delete link
The system SHALL provide a delete button on each link row that removes the link via the API.

#### Scenario: Delete a link from the card
- **WHEN** the user clicks the delete button on a link
- **THEN** the link is removed via the API and disappears from the card
