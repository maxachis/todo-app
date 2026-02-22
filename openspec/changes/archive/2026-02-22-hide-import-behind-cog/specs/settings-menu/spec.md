## ADDED Requirements

### Requirement: Settings cog button in navigation bar
The system SHALL display a cog/settings icon button in the top navigation bar, positioned immediately before the theme toggle button. The button SHALL use the gear emoji to match the existing icon style.

#### Scenario: Cog button renders in navbar
- **WHEN** the navigation bar renders
- **THEN** a cog button with a gear icon is displayed to the left of the theme toggle button

#### Scenario: Cog button is visible on all viewports
- **WHEN** the viewport is any width (desktop or mobile)
- **THEN** the cog button is visible in the top navigation bar

### Requirement: Settings dropdown menu
The system SHALL open a dropdown menu when the cog button is clicked. The dropdown SHALL contain navigation links for utility actions, starting with an "Import" link.

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

### Requirement: Dropdown dismissal
The system SHALL close the settings dropdown when the user clicks outside, presses Escape, or navigates to a new page.

#### Scenario: Click outside closes dropdown
- **WHEN** the dropdown is open and the user clicks anywhere outside the dropdown
- **THEN** the dropdown closes

#### Scenario: Escape key closes dropdown
- **WHEN** the dropdown is open and the user presses the Escape key
- **THEN** the dropdown closes

#### Scenario: Navigation closes dropdown
- **WHEN** the dropdown is open and the user navigates to a different page
- **THEN** the dropdown closes
