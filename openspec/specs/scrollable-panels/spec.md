## ADDED Requirements

### Requirement: Viewport-locked app shell
The app shell SHALL fill exactly the viewport height. The document body SHALL NOT produce a scrollbar on desktop viewports (above 1023px width).

#### Scenario: No document scroll on desktop
- **WHEN** the app is viewed on a viewport wider than 1023px with any amount of content in any page
- **THEN** the browser document SHALL NOT scroll; all scrolling occurs within individual panels

#### Scenario: Normal document scroll on mobile
- **WHEN** the app is viewed on a viewport 1023px or narrower
- **THEN** the page SHALL scroll normally as a single document (existing mobile behavior preserved)

### Requirement: Tasks page panels scroll independently
On the Tasks page, the sidebar, center task list, and detail panel SHALL each scroll independently when their content overflows.

#### Scenario: Center task list overflows
- **WHEN** the task list contains more items than fit in the visible panel area
- **THEN** the center panel SHALL show a vertical scrollbar and scroll independently while the sidebar and detail panel remain stationary

#### Scenario: Detail panel overflows
- **WHEN** a task's detail content (notes, fields) exceeds the visible panel area
- **THEN** the detail panel SHALL scroll independently while the sidebar and center panel remain stationary

#### Scenario: Sidebar overflows
- **WHEN** the list sidebar contains more lists than fit in the visible area
- **THEN** the sidebar SHALL scroll independently while the center and detail panels remain stationary

### Requirement: Network pages panels scroll independently
On the People, Organizations, and Interactions pages, the list panel and detail panel SHALL each scroll independently when their content overflows.

#### Scenario: People list overflows
- **WHEN** the people list contains more entries than fit in the visible list panel
- **THEN** the list panel SHALL scroll independently while the detail panel remains stationary

#### Scenario: Detail panel overflows on network pages
- **WHEN** the detail form and linked tasks section exceed the visible detail panel area
- **THEN** the detail panel SHALL scroll independently while the list panel remains stationary

### Requirement: Relationships page columns scroll independently
On the Relationships page, the Person-Person column and Organization-Person column SHALL each scroll independently.

#### Scenario: Person relationships column overflows
- **WHEN** the person-to-person relationships list exceeds the visible column area
- **THEN** that column SHALL scroll independently while the other column remains stationary

### Requirement: Header remains visible
The top navigation header SHALL remain visible at all times on desktop viewports, regardless of content scrolling within panels.

#### Scenario: Header stays pinned during panel scroll
- **WHEN** the user scrolls within any panel on any page
- **THEN** the top navigation header SHALL remain in its fixed position at the top of the viewport
