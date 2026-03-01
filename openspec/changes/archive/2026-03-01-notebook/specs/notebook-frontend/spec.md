## ADDED Requirements

### Requirement: Notebook route with two-panel layout
The system SHALL provide a `/notebook` route with a two-panel layout: a page sidebar (left) and an editor area (right). The sidebar SHALL display a "New Page" button, a "Today" button, and a list of pages grouped into "Recent" (wiki pages, by updated_at) and "Daily" (daily pages, by date descending). Clicking a page in the sidebar SHALL load it in the editor. The URL SHALL update to `/notebook/{slug}` when a page is selected.

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
