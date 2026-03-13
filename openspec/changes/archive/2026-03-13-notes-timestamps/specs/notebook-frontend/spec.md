## ADDED Requirements

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
