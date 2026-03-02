### Requirement: Mobile toggle buttons only visible on Tasks route
The system SHALL hide the sidebar toggle (☰) and detail-panel toggle (⋮) buttons when the user is not on the Tasks route (`/`).

#### Scenario: Buttons visible on Tasks route at mobile breakpoint
- **WHEN** the user is on the Tasks route (`/`) at a viewport width ≤ 1023px
- **THEN** both the sidebar toggle and detail-panel toggle buttons are rendered in the navbar

#### Scenario: Buttons hidden on non-Tasks routes at mobile breakpoint
- **WHEN** the user navigates to any route other than `/` at a viewport width ≤ 1023px
- **THEN** neither the sidebar toggle nor the detail-panel toggle button is rendered in the navbar

#### Scenario: Buttons remain hidden on desktop regardless of route
- **WHEN** the user is on any route at a viewport width ≥ 1024px
- **THEN** neither toggle button is visible (unchanged existing behavior via CSS)
