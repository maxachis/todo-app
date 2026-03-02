## MODIFIED Requirements

### Requirement: Notebook route with two-panel layout
The system SHALL provide a `/notebook` route with a two-panel layout: a page sidebar (left) and an editor area (right). The sidebar SHALL display a "New Page" button, a "Today" button, and a list of pages grouped into "Recent" (wiki pages, by updated_at) and "Daily" (daily pages, by date descending). Clicking a page in the sidebar SHALL load it in the editor. The URL SHALL update to `/notebook/{slug}` when a page is selected. The sidebar SHALL be collapsible via a toggle button or keyboard shortcut (`Cmd/Ctrl+\`). When collapsed, the sidebar SHALL reduce to a slim strip with an expand button, and the editor SHALL fill the full width. The collapsed state SHALL persist in localStorage.

#### Scenario: Notebook route loads with empty state
- **WHEN** the user navigates to `/notebook` with no pages
- **THEN** the sidebar shows "New Page" and "Today" buttons with no page list, and the editor shows an empty state message

#### Scenario: Sidebar lists pages grouped by type
- **WHEN** the user navigates to `/notebook` and pages exist
- **THEN** the sidebar shows wiki pages under "Recent" (sorted by updated_at desc) and daily pages under "Daily" (sorted by date desc)

#### Scenario: Selecting a page loads it in the editor
- **WHEN** the user clicks a page in the sidebar
- **THEN** the editor loads the page content and the URL updates to `/notebook/{slug}`

#### Scenario: Direct URL navigation to a page
- **WHEN** the user navigates to `/notebook/migration-runbook`
- **THEN** the page with slug `migration-runbook` loads in the editor and is highlighted in the sidebar

#### Scenario: Sidebar collapsed on load
- **WHEN** the user navigates to `/notebook` and the sidebar was previously collapsed
- **THEN** the layout shows the editor at full width with a slim sidebar strip containing the expand button
