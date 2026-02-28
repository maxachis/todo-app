## MODIFIED Requirements

### Requirement: Settings dropdown menu
The system SHALL open a dropdown menu when the cog button is clicked. The dropdown SHALL contain navigation links for utility actions, starting with an "Import" link, and an "Export Database" action that triggers a full database download. Below a visual divider, the dropdown SHALL contain a "Completion Sound" preference selector with the user's current sound choice.

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

#### Scenario: Dropdown contains completion sound selector
- **WHEN** the dropdown menu is open
- **THEN** a visual divider separates the link items from a "Completion Sound" label with a select dropdown showing the current sound preference

#### Scenario: Changing completion sound in dropdown
- **WHEN** the user selects a different sound from the completion sound selector
- **THEN** the preference updates immediately, persists to localStorage, and the selected sound plays as a preview
