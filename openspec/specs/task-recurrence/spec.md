### Requirement: Recurrence rule storage on tasks
The system SHALL store recurrence configuration on the Task model using a `recurrence_type` field (choices: `none`, `daily`, `weekly`, `monthly`, `yearly`, `custom_dates`) and a `recurrence_rule` JSONField containing type-specific parameters.

#### Scenario: Task with no recurrence
- **WHEN** a task is created without recurrence fields
- **THEN** `recurrence_type` defaults to `none` and `recurrence_rule` defaults to `{}`

#### Scenario: Task with weekly recurrence
- **WHEN** a task has `recurrence_type` set to `weekly` and `recurrence_rule` set to `{"days": [0, 2, 4]}`
- **THEN** the task is configured to repeat on Monday, Wednesday, and Friday (ISO weekday: 0=Monday)

#### Scenario: Task with yearly recurrence
- **WHEN** a task has `recurrence_type` set to `yearly` and `recurrence_rule` set to `{"month": 3, "day": 15}`
- **THEN** the task is configured to repeat every March 15

#### Scenario: Task with custom annual dates
- **WHEN** a task has `recurrence_type` set to `custom_dates` and `recurrence_rule` set to `{"dates": ["03-15", "06-15", "09-15", "12-15"]}`
- **THEN** the task is configured to repeat on those four dates each year

#### Scenario: Task with monthly recurrence
- **WHEN** a task has `recurrence_type` set to `monthly` and `recurrence_rule` set to `{"day_of_month": 15}`
- **THEN** the task is configured to repeat on the 15th of every month

#### Scenario: Task with daily recurrence
- **WHEN** a task has `recurrence_type` set to `daily` and `recurrence_rule` set to `{}`
- **THEN** the task is configured to repeat every day

### Requirement: Next occurrence generation on completion
The system SHALL create a new task instance when a recurring task is completed. The new task SHALL copy the title, notes, priority, tags, section, and recurrence rule from the completed task, with a new `due_date` computed as the next occurrence after today.

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

### Requirement: Recurrence rule validation
The system SHALL validate recurrence rule data when creating or updating a task's recurrence settings.

#### Scenario: Invalid weekday in weekly rule
- **WHEN** a task update sets `recurrence_type=weekly` with `recurrence_rule={"days": [7]}`
- **THEN** the system rejects the request with a 422 error (valid days are 0-6)

#### Scenario: Invalid day of month in monthly rule
- **WHEN** a task update sets `recurrence_type=monthly` with `recurrence_rule={"day_of_month": 32}`
- **THEN** the system rejects the request with a 422 error (valid days are 1-31)

#### Scenario: Invalid date format in custom dates
- **WHEN** a task update sets `recurrence_type=custom_dates` with `recurrence_rule={"dates": ["2026-03-15"]}`
- **THEN** the system rejects the request with a 422 error (expected MM-DD format)

#### Scenario: Empty days list in weekly rule
- **WHEN** a task update sets `recurrence_type=weekly` with `recurrence_rule={"days": []}`
- **THEN** the system rejects the request with a 422 error (at least one day required)

#### Scenario: Custom dates list capped at 52 entries
- **WHEN** a task update sets `recurrence_type=custom_dates` with more than 52 dates
- **THEN** the system rejects the request with a 422 error

### Requirement: Clearing recurrence
The system SHALL allow removing recurrence from a task by setting `recurrence_type` to `none`.

#### Scenario: Clear recurrence from a recurring task
- **WHEN** a task with `recurrence_type=weekly` is updated with `recurrence_type=none`
- **THEN** the task's `recurrence_type` becomes `none`, `recurrence_rule` becomes `{}`, and subsequent completions do not generate new occurrences
