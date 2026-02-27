## MODIFIED Requirements

### Requirement: Settings dropdown menu
The system SHALL open a dropdown menu when the cog button is clicked. The dropdown SHALL contain navigation links for utility actions, starting with an "Import" link, and an "Export Database" action that triggers a full database download.

#### Scenario: Clicking cog opens dropdown
- **WHEN** the user clicks the cog button
- **THEN** a dropdown menu appears below the button, anchored to the right edge

#### Scenario: Dropdown contains Import link
- **WHEN** the dropdown menu is open
- **THEN** the menu contains an "Import" link that navigates to `/import`

#### Scenario: Clicking Import navigates and closes dropdown
- **WHEN** the user clicks the "Import" link in the dropdown
- **THEN** the browser navigates to `/import` and the dropdown closes

#### Scenario: Active state on Import route
- **WHEN** the user is on the `/import` route
- **THEN** the "Import" link in the dropdown is visually marked as active

#### Scenario: Dropdown contains Export Database action
- **WHEN** the dropdown menu is open
- **THEN** the menu contains an "Export Database" action below the "Import" link

#### Scenario: Clicking Export Database triggers download
- **WHEN** the user clicks the "Export Database" action in the dropdown
- **THEN** the browser initiates a file download from `/api/export/full/` and the dropdown closes
