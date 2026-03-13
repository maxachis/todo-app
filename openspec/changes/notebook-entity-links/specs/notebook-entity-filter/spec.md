## ADDED Requirements

### Requirement: Filter pages by entity via API
The page list endpoint `GET /api/notebook/pages/` SHALL accept optional `entity_type` (string) and `entity_id` (integer) query parameters. When both are provided, the endpoint SHALL return only pages that have a `PageEntityMention` matching the given entity_type and entity_id. The entity_type parameter SHALL accept "person" and "organization". When entity filter params are provided alongside `search` or `page_type`, all filters SHALL be combined (AND logic). When entity filter params are absent, behavior SHALL be unchanged.

#### Scenario: Filter pages by person
- **WHEN** a GET request is made to `/api/notebook/pages/?entity_type=person&entity_id=7`
- **THEN** the response contains only pages that have a PageEntityMention with entity_type="person" and entity_id=7, sorted by updated_at descending

#### Scenario: Filter pages by organization
- **WHEN** a GET request is made to `/api/notebook/pages/?entity_type=organization&entity_id=3`
- **THEN** the response contains only pages that have a PageEntityMention with entity_type="organization" and entity_id=3

#### Scenario: Entity filter combined with search
- **WHEN** a GET request is made to `/api/notebook/pages/?entity_type=person&entity_id=7&search=meeting`
- **THEN** the response contains only pages mentioning person 7 whose title contains "meeting"

#### Scenario: Entity filter with no matches
- **WHEN** a GET request is made with entity_type and entity_id that no page mentions
- **THEN** the response is an empty list

#### Scenario: Missing entity_id with entity_type
- **WHEN** a GET request includes `entity_type` but not `entity_id`
- **THEN** the entity filter is ignored and all pages are returned (same as no filter)

### Requirement: Entity filter UI in notebook sidebar
The notebook sidebar SHALL display an entity filter control above the page list. The filter SHALL use a TypeaheadSelect component that allows the user to search and select a person or organization. Options SHALL be grouped by type ("People" and "Organizations"). When an entity is selected, the page list SHALL update to show only pages mentioning that entity. A clear/reset button SHALL be visible when a filter is active, allowing the user to return to the unfiltered view.

#### Scenario: Select person filter
- **WHEN** the user opens the entity filter and selects "John Smith" (person)
- **THEN** the sidebar page list updates to show only pages that mention John Smith, and a clear button appears

#### Scenario: Select organization filter
- **WHEN** the user opens the entity filter and selects "Acme Corp" (organization)
- **THEN** the sidebar page list updates to show only pages that mention Acme Corp

#### Scenario: Clear entity filter
- **WHEN** the user clicks the clear button on an active entity filter
- **THEN** the filter is removed and the sidebar returns to showing all pages

#### Scenario: Entity filter with sidebar search
- **WHEN** the user has an entity filter active and types in the sidebar search field
- **THEN** both filters apply — showing only pages matching both the entity and the search text

#### Scenario: Empty results with filter
- **WHEN** the user selects an entity that has no associated pages
- **THEN** the page list shows an empty state message like "No pages mention this entity"

### Requirement: Filter indicator
When an entity filter is active, the sidebar SHALL visually indicate that results are filtered. The selected entity name SHALL be displayed as a filter chip or label near the filter control.

#### Scenario: Active filter display
- **WHEN** the user has selected "John Smith" as the entity filter
- **THEN** the sidebar shows "John Smith" as a visible filter label/chip with a clear (x) button

#### Scenario: No filter active
- **WHEN** no entity filter is selected
- **THEN** no filter indicator is shown and the page list displays all pages normally
