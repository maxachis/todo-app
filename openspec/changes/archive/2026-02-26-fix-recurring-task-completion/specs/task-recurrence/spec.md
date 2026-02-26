## MODIFIED Requirements

### Requirement: Next occurrence generation on completion
The system SHALL create a new task instance when a recurring task is completed. The new task SHALL copy the title, notes, priority, tags, section, and recurrence rule from the completed task, with a new `due_date` computed as the next occurrence after today. The new task SHALL be positioned at the same position as the completed task.

#### Scenario: Complete a daily recurring task
- **WHEN** a task with `recurrence_type=daily` and `due_date=2026-02-20` is completed
- **THEN** a new task is created in the same section with `due_date=2026-02-21` and the same recurrence rule

#### Scenario: Complete a weekly recurring task
- **WHEN** a task with `recurrence_type=weekly`, `recurrence_rule={"days": [0, 4]}`, and `due_date=2026-02-20` (Friday) is completed on 2026-02-20
- **THEN** a new task is created with `due_date=2026-02-23` (next Monday)

#### Scenario: Complete a monthly recurring task
- **WHEN** a task with `recurrence_type=monthly`, `recurrence_rule={"day_of_month": 15}`, and `due_date=2026-02-15` is completed
- **THEN** a new task is created with `due_date=2026-03-15`

#### Scenario: Monthly recurrence clamps to last day of short month
- **WHEN** a task with `recurrence_type=monthly` and `recurrence_rule={"day_of_month": 31}` generates a next occurrence for February
- **THEN** the new task's `due_date` is clamped to February 28 (or 29 in a leap year)

#### Scenario: Complete a yearly recurring task
- **WHEN** a task with `recurrence_type=yearly`, `recurrence_rule={"month": 3, "day": 15}`, and `due_date=2026-03-15` is completed
- **THEN** a new task is created with `due_date=2027-03-15`

#### Scenario: Complete a custom-dates recurring task
- **WHEN** a task with `recurrence_type=custom_dates`, `recurrence_rule={"dates": ["03-15", "06-15", "09-15", "12-15"]}`, and `due_date=2026-03-15` is completed on 2026-03-20
- **THEN** a new task is created with `due_date=2026-06-15` (next date in the list after today)

#### Scenario: Custom dates wrap to next year
- **WHEN** a task with `recurrence_type=custom_dates`, `recurrence_rule={"dates": ["03-15", "06-15"]}`, and `due_date=2026-06-15` is completed on 2026-07-01
- **THEN** a new task is created with `due_date=2027-03-15` (wraps to first date in next year)

#### Scenario: Next occurrence copies tags
- **WHEN** a recurring task with tags `["urgent", "taxes"]` is completed
- **THEN** the new task instance has the same tags applied

#### Scenario: Next occurrence does not copy subtasks
- **WHEN** a recurring task with subtasks is completed
- **THEN** the new task instance has no subtasks

#### Scenario: Non-recurring task completion unchanged
- **WHEN** a task with `recurrence_type=none` is completed
- **THEN** no new task is generated (existing behavior preserved)

#### Scenario: Next occurrence is positioned in-place
- **WHEN** a recurring task at position 20 in a section is completed
- **THEN** the new task is created with the same position value (20), so it appears in the same location in the task list

## ADDED Requirements

### Requirement: Complete endpoint returns full next occurrence data
The `/tasks/{id}/complete/` API response SHALL include a `next_occurrence` field containing the full serialized task object of the newly created occurrence (or `null` if the task is not recurring). The existing `next_occurrence_id` field SHALL continue to be returned for backwards compatibility.

#### Scenario: Complete a recurring task returns next occurrence
- **WHEN** a recurring task is completed via `POST /tasks/{id}/complete/`
- **THEN** the response includes `next_occurrence_id` (integer) and `next_occurrence` (full task object with id, title, due_date, position, recurrence_type, etc.)

#### Scenario: Complete a non-recurring task returns null next occurrence
- **WHEN** a non-recurring task is completed via `POST /tasks/{id}/complete/`
- **THEN** the response includes `next_occurrence_id: null` and `next_occurrence: null`

### Requirement: Optimistic UI update on task completion
The frontend SHALL update the task store optimistically on completion without performing a full list re-fetch. The completed task SHALL be updated in-place in the store, and the next occurrence (if any) SHALL be inserted into the same section.

#### Scenario: Completing a task does not cause a page flash
- **WHEN** a user completes any task (recurring or not) on the Tasks page
- **THEN** the task list updates smoothly without a visible blank/flash, the completed task moves to the "Completed" section, and no full list re-fetch occurs

#### Scenario: Completing a recurring task shows new occurrence in-place
- **WHEN** a user completes a recurring task that was positioned between Task A and Task C
- **THEN** the new occurrence appears between Task A and Task C (same position in the active list)

### Requirement: Undo recurring task completion cleans up next occurrence
When undoing the completion of a recurring task, the system SHALL delete the next occurrence that was created during completion, in addition to un-completing the original task.

#### Scenario: Undo completion of recurring task
- **WHEN** a user completes a recurring task and then clicks "Undo" on the completion toast
- **THEN** the next occurrence task is deleted AND the original task is un-completed, resulting in exactly one copy of the recurring task in its original state

#### Scenario: Undo completion of non-recurring task
- **WHEN** a user completes a non-recurring task and then clicks "Undo"
- **THEN** the task is un-completed normally (no next occurrence to clean up)
