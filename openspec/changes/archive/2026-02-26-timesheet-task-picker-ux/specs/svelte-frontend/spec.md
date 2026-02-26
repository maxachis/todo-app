## MODIFIED Requirements

### Requirement: Timesheet page
The system SHALL provide a dedicated page at `/timesheet` for weekly time tracking with navigation and summaries. The task selector SHALL use a hierarchical checkbox-based picker that displays tasks with indentation reflecting their parent-child nesting, replacing the native `<select multiple>`. Time entry rows SHALL display associated task names with hierarchy breadcrumbs instead of omitting task information. On phone viewports (640px and below), the summary bar, entry form, week navigation, and entry rows SHALL wrap/stack to prevent horizontal overflow.

#### Scenario: Weekly view with navigation
- **WHEN** the user navigates to `/timesheet`
- **THEN** the page shows the current week's time entries with previous/next week navigation

#### Scenario: Summary bar
- **WHEN** viewing a week's timesheet
- **THEN** a summary bar shows total hours and per-project breakdowns

#### Scenario: Week bounds are Sunday through Saturday
- **WHEN** a week is loaded in the timesheet view
- **THEN** the range begins on Sunday and ends on Saturday

#### Scenario: Create time entry
- **WHEN** the user fills in the time entry form (project, date, description, optional tasks) and submits
- **THEN** the entry is created and appears in the appropriate date group

#### Scenario: Entry rows display local creation time
- **WHEN** timesheet entries are listed
- **THEN** each row shows the entry creation time in the user's local device time

#### Scenario: Task selector shows hierarchical tree by project
- **WHEN** the user selects a project in the time entry form
- **THEN** a checkbox-based task picker shows incomplete tasks from that project's linked lists, indented by their nesting depth

#### Scenario: Entry rows display associated task names
- **WHEN** timesheet entries with linked tasks are listed
- **THEN** each entry row displays task names with parent hierarchy breadcrumbs

#### Scenario: Phone viewport summary bar wraps
- **WHEN** the viewport is 640px or narrower
- **THEN** the summary bar items wrap to multiple lines instead of overflowing horizontally

#### Scenario: Phone viewport entry form stacks
- **WHEN** the viewport is 640px or narrower
- **THEN** the time entry form fields stack vertically to fit the narrow viewport

#### Scenario: Phone viewport week navigation fits
- **WHEN** the viewport is 640px or narrower
- **THEN** the week navigation (prev/next buttons and date range) fits within the viewport without overflow

#### Scenario: Phone viewport entry rows wrap
- **WHEN** the viewport is 640px or narrower
- **THEN** entry row content (project, time, description, tasks, delete button) wraps to fit without horizontal overflow
