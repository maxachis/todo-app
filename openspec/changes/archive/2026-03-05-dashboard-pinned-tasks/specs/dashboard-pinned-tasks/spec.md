## ADDED Requirements

### Requirement: Dashboard displays a Pinned tasks group
The Dashboard Upcoming tab SHALL display a "Pinned" group containing all incomplete pinned tasks. This group SHALL appear above the time-horizon groups (Overdue, Today, Tomorrow, This Week, Later) but below the Follow-ups Due section. Pinned tasks with due dates SHALL appear in both the Pinned group and their corresponding time-horizon group.

#### Scenario: Pinned tasks without due dates are shown
- **WHEN** the user navigates to `/dashboard`
- **AND** there are incomplete pinned tasks without due dates
- **THEN** the Pinned group is displayed with those tasks

#### Scenario: Pinned tasks with due dates appear in both groups
- **WHEN** the user navigates to `/dashboard`
- **AND** there is an incomplete pinned task with a due date of today
- **THEN** the task appears in the Pinned group
- **AND** the task appears in the Today group

#### Scenario: No pinned tasks exist
- **WHEN** the user navigates to `/dashboard`
- **AND** no incomplete tasks are pinned
- **THEN** the Pinned group is not displayed

#### Scenario: Pinned group sort order
- **WHEN** the Pinned group contains multiple tasks
- **THEN** tasks SHALL be sorted by priority descending (highest first)
- **AND** tasks with equal priority SHALL be sorted by title alphabetically
- **AND** tasks with due dates SHALL sort before tasks without due dates

### Requirement: Pinned tasks display a pin indicator in time-horizon groups
When a pinned task appears in a time-horizon group (Overdue, Today, etc.), it SHALL display a pin icon indicator to distinguish it from non-pinned tasks.

#### Scenario: Pinned task in Today group shows pin icon
- **WHEN** a pinned task with today's due date appears in the Today group
- **THEN** the task row displays a pin icon next to the title
