## ADDED Requirements

### Requirement: Dark color palette via CSS variable overrides
The system SHALL define a dark theme by overriding all CSS custom properties under `:root[data-theme="dark"]`. The dark palette SHALL use warm dark tones (not pure black) to maintain visual consistency with the light theme's earthy character.

#### Scenario: Dark variables override light defaults
- **WHEN** the `<html>` element has `data-theme="dark"`
- **THEN** all CSS custom properties (backgrounds, text, borders, accents, shadows, status colors, pinned colors, tag colors) reflect dark-appropriate values

#### Scenario: Light theme remains the default
- **WHEN** no `data-theme` attribute is set on `<html>`
- **THEN** the existing light color palette applies unchanged

#### Scenario: All components respond to theme change
- **WHEN** the theme switches from light to dark or vice versa
- **THEN** all UI surfaces, text, borders, and interactive elements update without page reload

### Requirement: Theme preference store
The system SHALL manage the user's theme preference in a Svelte writable store with three possible values: `light`, `dark`, and `system`. The store SHALL sync with `localStorage` and the `data-theme` attribute on `<html>`.

#### Scenario: Store initializes from localStorage
- **WHEN** the app loads
- **THEN** the theme store reads the saved preference from `localStorage` key `theme`, defaulting to `system` if no value is stored

#### Scenario: Store persists preference changes
- **WHEN** the user changes the theme preference via the toggle
- **THEN** the new value is written to `localStorage` and the `data-theme` attribute updates immediately

#### Scenario: System preference follows OS setting
- **WHEN** the theme preference is set to `system`
- **THEN** the resolved theme matches the OS `prefers-color-scheme` value (dark or light)

#### Scenario: System preference responds to OS changes
- **WHEN** the theme preference is `system` and the user changes their OS color scheme
- **THEN** the app theme updates to match without requiring a page reload

### Requirement: FOUC prevention on page load
The system SHALL prevent a flash of incorrect theme by setting the `data-theme` attribute on `<html>` via an inline script in `<head>` before any stylesheets or body content render.

#### Scenario: Dark mode user sees no light flash
- **WHEN** a user with a saved `dark` preference loads the page
- **THEN** the page renders in dark mode from the first paint with no visible flash of light theme

#### Scenario: System-preference user sees correct theme immediately
- **WHEN** a user with no saved preference (or `system`) loads the page and their OS is set to dark
- **THEN** the page renders in dark mode from the first paint

### Requirement: Theme toggle control in navigation bar
The system SHALL display a theme toggle control in the top navigation bar that allows switching between light, system, and dark modes. The toggle SHALL be accessible via keyboard.

#### Scenario: Toggle displays current theme state
- **WHEN** the app renders the navigation bar
- **THEN** the theme toggle shows an icon or label reflecting the current preference (light, system, or dark)

#### Scenario: Cycling through theme options
- **WHEN** the user clicks the theme toggle
- **THEN** the preference cycles through light → system → dark → light

#### Scenario: Toggle is keyboard accessible
- **WHEN** the user focuses the theme toggle and presses Enter or Space
- **THEN** the theme cycles to the next option, same as a click

#### Scenario: Toggle is visible on all pages
- **WHEN** the user navigates to any page (Tasks, Projects, Timesheet, Import)
- **THEN** the theme toggle remains visible in the top navigation bar
