### Requirement: Timesheet API summary includes weekly totals
The timesheet GET endpoint SHALL return a `summary` object containing `total_hours` (integer count of time entries for the requested week) and a `per_project` array. Each `per_project` item SHALL contain `project_id`, `project_name`, and `hours` (integer count of that project's entries for the week). The `per_project` array SHALL be ordered by descending weekly hours.

#### Scenario: Summary reflects weekly entry counts
- **WHEN** the timesheet is requested for a week with 5 entries across 2 projects (3 for Project A, 2 for Project B)
- **THEN** `summary.total_hours` is 5, and `per_project` contains Project A with `hours: 3` and Project B with `hours: 2`

#### Scenario: Empty week returns zero totals
- **WHEN** the timesheet is requested for a week with no entries
- **THEN** `summary.total_hours` is 0 and `per_project` is an empty array

### Requirement: Timesheet API summary includes overall (all-time) totals
The timesheet GET endpoint SHALL include `overall_total_hours` in the `summary` object, representing the total count of all time entries across all dates. Each item in `per_project` SHALL include an `overall_hours` field representing the total count of that project's time entries across all dates.

#### Scenario: Overall totals reflect all-time data
- **WHEN** Project A has 42 total time entries across all weeks and 3 entries in the current week
- **THEN** the `per_project` entry for Project A has `hours: 3` and `overall_hours: 42`

#### Scenario: Overall total hours sums all entries
- **WHEN** there are 120 total time entries across all projects and dates, and 5 entries in the current week
- **THEN** `summary.total_hours` is 5 and `summary.overall_total_hours` is 120

### Requirement: Projects with zero weekly hours but nonzero overall hours appear in per_project
The `per_project` array SHALL include projects that have time entries in other weeks but zero entries in the requested week. These entries SHALL have `hours: 0` and their `overall_hours` value. The array SHALL be ordered by descending weekly hours, then by descending overall hours for projects with equal weekly hours.

#### Scenario: Inactive-this-week project appears with zero weekly hours
- **WHEN** Project C has 10 all-time entries but none in the current week
- **THEN** `per_project` includes Project C with `hours: 0` and `overall_hours: 10`

#### Scenario: Sort order places weekly-active projects first
- **WHEN** Project A has 3 weekly hours and 20 overall, Project B has 0 weekly hours and 50 overall
- **THEN** Project A appears before Project B in `per_project`

### Requirement: Summary bar displays weekly and overall hours
The timesheet frontend summary bar SHALL display `total_hours` as the primary total and `overall_total_hours` in parentheses (e.g., "Total: 5h (120h total)"). Each per-project item SHALL display weekly hours with overall hours in parentheses (e.g., "Project A: 3h (42h total)").

#### Scenario: Summary bar shows both weekly and overall totals
- **WHEN** the timesheet loads with `total_hours: 5` and `overall_total_hours: 120`
- **THEN** the summary bar displays "Total: 5h (120h total)"

#### Scenario: Per-project display includes overall hours
- **WHEN** Project A has `hours: 3` and `overall_hours: 42`
- **THEN** the summary bar shows "Project A: 3h (42h total)"

#### Scenario: Project with zero weekly hours still appears
- **WHEN** Project C has `hours: 0` and `overall_hours: 10`
- **THEN** the summary bar shows "Project C: 0h (10h total)"
