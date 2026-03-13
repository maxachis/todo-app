# Notebook Frontend

## Purpose

Svelte frontend UI for the notebook feature, including the two-panel layout, page creation, textarea editor with auto-save, and typeahead mention insertion for people and entities.

## Requirements

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

### Requirement: New Page creation
The "New Page" button SHALL create a new wiki page. Clicking it SHALL immediately create a page via the API with a default title (e.g., "Untitled"), navigate to it, and place the cursor in the title field for immediate renaming.

#### Scenario: Create new wiki page
- **WHEN** the user clicks "New Page"
- **THEN** a new wiki page is created, appears in the sidebar, loads in the editor, and the title field is focused for editing

### Requirement: Today button creates or opens daily page
The "Today" button SHALL create a daily page for today's date if one doesn't exist, or open the existing one. It SHALL use the get-or-create behavior of the API.

#### Scenario: Today page doesn't exist
- **WHEN** the user clicks "Today" and no daily page exists for today
- **THEN** a daily page is created with today's date and opens in the editor

#### Scenario: Today page already exists
- **WHEN** the user clicks "Today" and a daily page for today already exists
- **THEN** the existing page opens in the editor

### Requirement: Textarea editor with auto-save
The editor area SHALL display the page title as an editable text input and the page content as an auto-expanding textarea. Changes to title or content SHALL auto-save via the API on blur or after a 1-second debounced typing pause. A subtle save indicator SHALL show when saving is in progress.

#### Scenario: Edit title and auto-save
- **WHEN** the user edits the page title and blurs the title input
- **THEN** the title is saved via the API and the sidebar updates to reflect the new title

#### Scenario: Edit content with debounced auto-save
- **WHEN** the user types in the content textarea and pauses for 1 second
- **THEN** the content is saved via the API, entity mentions are re-extracted, and the save indicator flashes briefly

#### Scenario: Textarea auto-expands
- **WHEN** the user types content that exceeds the textarea height
- **THEN** the textarea grows vertically to fit the content without scrollbars within the textarea itself

### Requirement: @ typeahead for people mentions
When the user types `@` followed by characters in the content textarea, a floating typeahead dropdown SHALL appear showing matching people (filtered by first/last name). Selecting a result SHALL insert `@[person:ID|First Last]` at the cursor position, replacing the `@query` text. Pressing Escape or clicking outside SHALL dismiss the typeahead without inserting.

#### Scenario: Trigger people typeahead
- **WHEN** the user types `@Jo` in the textarea
- **THEN** a floating dropdown appears showing people matching "Jo" (e.g., "John Smith", "Joanna Lee")

#### Scenario: Select person from typeahead
- **WHEN** the user selects "John Smith" (id: 7) from the typeahead
- **THEN** the text `@Jo` is replaced with `@[person:7|John Smith]` and the typeahead closes

#### Scenario: Dismiss typeahead with Escape
- **WHEN** the user presses Escape while the typeahead is open
- **THEN** the typeahead closes and the typed text remains unchanged

#### Scenario: Navigate typeahead with keyboard
- **WHEN** the typeahead is open and the user presses Arrow Down/Up
- **THEN** the highlight moves through results; Enter selects the highlighted result

#### Scenario: @ at word boundary only
- **WHEN** the user types `email@example` (@ not at a word boundary)
- **THEN** the typeahead does NOT trigger

### Requirement: [[ typeahead for entity and page mentions
When the user types `[[` followed by characters in the content textarea, a floating typeahead dropdown SHALL appear showing matching entities across pages, tasks, organizations, and projects. Results SHALL be grouped by type with type badges. Selecting a result SHALL insert `[[type:ID|Title]]` at the cursor position, replacing the `[[query` text and appending `]]`. Pressing Escape SHALL dismiss the typeahead.

#### Scenario: Trigger entity typeahead
- **WHEN** the user types `[[migr` in the textarea
- **THEN** a floating dropdown appears showing matching entities grouped by type (e.g., page "Migration Runbook", task "Migrate DB to PG")

#### Scenario: Select page from typeahead
- **WHEN** the user selects page "Migration Runbook" (id: 12) from the typeahead
- **THEN** the text `[[migr` is replaced with `[[page:12|Migration Runbook]]` and the typeahead closes

#### Scenario: Select task from typeahead
- **WHEN** the user selects task "Deploy fix" (id: 189) from the typeahead
- **THEN** the text is replaced with `[[task:189|Deploy fix]]`

#### Scenario: Select organization from typeahead
- **WHEN** the user selects organization "Acme Corp" (id: 3) from the typeahead
- **THEN** the text is replaced with `[[org:3|Acme Corp]]`

#### Scenario: Results grouped by type with badges
- **WHEN** the `[[` typeahead shows results
- **THEN** results are grouped under type headers (Pages, Tasks, Organizations, Projects) with a type icon/badge next to each result

#### Scenario: Empty results
- **WHEN** the user types `[[xyznonexistent` and no entities match
- **THEN** the dropdown shows "No results" and the user can dismiss with Escape

### Requirement: Timestamps displayed on sidebar page items
Each page item in the notebook sidebar SHALL display a timestamp below or beside the page title. The timestamp SHALL show the `updated_at` value formatted as a relative time (e.g., "2h ago", "3d ago") for recent pages (within the last 7 days) and as a short date (e.g., "Mar 5") for older pages. The full datetime SHALL be available as a tooltip on hover via the `title` HTML attribute (e.g., "Mar 5, 2026 2:30 PM").

#### Scenario: Recently updated page shows relative time
- **WHEN** a page was last updated 2 hours ago
- **THEN** the sidebar item SHALL display "2h ago" as the timestamp

#### Scenario: Older page shows short date
- **WHEN** a page was last updated on March 5 (more than 7 days ago)
- **THEN** the sidebar item SHALL display "Mar 5" as the timestamp

#### Scenario: Timestamp tooltip shows full datetime
- **WHEN** the user hovers over a sidebar item's timestamp
- **THEN** a tooltip SHALL display the full datetime (e.g., "Mar 5, 2026 2:30 PM")

### Requirement: Timestamps displayed in page editor metadata
The page editor area SHALL display both the created and last-updated timestamps in a metadata line below the page title or above the editor content. The format SHALL be absolute (e.g., "Created: Mar 5, 2026 2:30 PM · Updated: Mar 10, 2026 4:15 PM"). For pages where `created_at` and `updated_at` are the same (never edited after creation), only "Created: ..." SHALL be shown.

#### Scenario: Page with edits shows both timestamps
- **WHEN** a page was created on Mar 5 and last updated on Mar 10
- **THEN** the metadata line SHALL display "Created: Mar 5, 2026 2:30 PM · Updated: Mar 10, 2026 4:15 PM"

#### Scenario: Never-edited page shows only created timestamp
- **WHEN** a page's created_at and updated_at are within 1 second of each other
- **THEN** the metadata line SHALL display only "Created: Mar 5, 2026 2:30 PM"

### Requirement: Sidebar timestamp reflects current sort field
When the sort order is changed to "Date created", the sidebar item timestamps SHALL switch to showing the `created_at` value instead of `updated_at`. When sort is "Last updated" or "Title", the sidebar SHALL show `updated_at`.

#### Scenario: Sort by created shows created timestamps
- **WHEN** the user selects "Date created" sort order
- **THEN** sidebar item timestamps SHALL display the `created_at` value

#### Scenario: Sort by title shows updated timestamps
- **WHEN** the user selects "Title" sort order
- **THEN** sidebar item timestamps SHALL display the `updated_at` value
