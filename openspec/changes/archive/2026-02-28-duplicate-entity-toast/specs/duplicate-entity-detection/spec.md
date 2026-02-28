## ADDED Requirements

### Requirement: API rejects duplicate person creation with 409
The `POST /api/people/` endpoint SHALL check for an existing person with the same `first_name` and `last_name` (case-insensitive) before creating. If a match exists, the endpoint MUST return HTTP 409 with a JSON body `{ "detail": "A person named <First> <Last> already exists." }` and MUST NOT create a new record.

#### Scenario: Creating a person with a name that already exists
- **WHEN** a POST request is made to `/api/people/` with `first_name` "John" and `last_name` "Smith" and a person with first_name "john" and last_name "smith" already exists
- **THEN** the API returns HTTP 409 with body `{ "detail": "A person named John Smith already exists." }` and no new person is created

#### Scenario: Creating a person with a unique name
- **WHEN** a POST request is made to `/api/people/` with `first_name` "Jane" and `last_name` "Doe" and no person with that name exists
- **THEN** the API returns HTTP 201 with the created person (existing behavior unchanged)

### Requirement: API rejects duplicate organization creation with 409
The `POST /api/organizations/` endpoint SHALL check for an existing organization with the same `name` (case-insensitive) before creating. If a match exists, the endpoint MUST return HTTP 409 with a JSON body `{ "detail": "An organization named <Name> already exists." }` and MUST NOT create a new record.

#### Scenario: Creating an organization with a name that already exists
- **WHEN** a POST request is made to `/api/organizations/` with `name` "Acme Corp" and an organization named "acme corp" already exists
- **THEN** the API returns HTTP 409 with body `{ "detail": "An organization named Acme Corp already exists." }` and no new organization is created

#### Scenario: Creating an organization with a unique name
- **WHEN** a POST request is made to `/api/organizations/` with `name` "New Corp" and no organization with that name exists
- **THEN** the API returns HTTP 201 with the created organization (existing behavior unchanged)

### Requirement: Frontend displays toast on duplicate person
When the person creation API returns 409, the frontend SHALL display a warning toast with the duplicate message and MUST NOT clear the form fields.

#### Scenario: User submits a duplicate person
- **WHEN** the user fills in the person form with a name that already exists and clicks "+ Person"
- **THEN** a toast notification of type "error" appears with the message from the 409 response, and the form fields remain populated with the user's input

### Requirement: Frontend displays toast on duplicate organization
When the organization creation API returns 409, the frontend SHALL display a warning toast with the duplicate message and MUST NOT clear the form fields.

#### Scenario: User submits a duplicate organization
- **WHEN** the user fills in the organization form with a name that already exists and clicks "+ Organization"
- **THEN** a toast notification of type "error" appears with the message from the 409 response, and the form fields remain populated with the user's input
