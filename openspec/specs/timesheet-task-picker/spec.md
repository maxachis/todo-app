### Requirement: Hierarchical task picker displays task tree with indentation
The timesheet task picker SHALL display tasks in a hierarchical tree structure with visual indentation indicating parent-child relationships. Top-level tasks SHALL have no indentation. Each level of nesting SHALL increase the left indentation. Visual indentation SHALL cap at 3 levels deep (tasks nested deeper than 3 levels SHALL render at the 3rd-level indent).

#### Scenario: Top-level tasks are not indented
- **WHEN** the task picker displays tasks from the selected project
- **THEN** top-level tasks (tasks with no parent) appear with no indentation

#### Scenario: Subtasks are indented under their parent
- **WHEN** the task picker displays a task that has a parent
- **THEN** the task is rendered with left indentation proportional to its depth in the hierarchy

#### Scenario: Deep nesting caps visual indent at 3 levels
- **WHEN** a task is nested 4 or more levels deep
- **THEN** it is displayed at the same indentation level as a 3rd-level task

### Requirement: Checkbox-based multi-select for tasks
The task picker SHALL use checkboxes for task selection instead of a native `<select multiple>`. Each task row SHALL have an independent checkbox. Checking or unchecking a parent task SHALL NOT automatically check or uncheck its children.

#### Scenario: Each task has an independent checkbox
- **WHEN** the task picker is displayed
- **THEN** each task row contains a checkbox that can be toggled independently

#### Scenario: Multiple tasks can be selected via checkboxes
- **WHEN** the user checks multiple task checkboxes
- **THEN** all checked task IDs are included in the time entry submission

#### Scenario: Parent selection does not cascade to children
- **WHEN** the user checks a parent task's checkbox
- **THEN** the child tasks' checkboxes remain unchanged

### Requirement: Task picker appears when project has tasks
The task picker SHALL appear only when the selected project has incomplete tasks available. When no project is selected or the project has no incomplete tasks, the task picker SHALL be hidden.

#### Scenario: Picker shown when project has tasks
- **WHEN** the user selects a project that has incomplete tasks in its linked lists
- **THEN** the hierarchical task picker is displayed

#### Scenario: Picker hidden when project has no tasks
- **WHEN** the user selects a project with no incomplete tasks
- **THEN** the task picker is not displayed

#### Scenario: Picker hidden when no project selected
- **WHEN** no project is selected in the entry form
- **THEN** the task picker is not displayed

### Requirement: Timesheet API returns task details in entries
The timesheet GET endpoint SHALL include `task_details` in each entry within `entries_by_date`. Each task detail object SHALL contain the task `id`, `title`, and `parent_titles` (an ordered list of ancestor task titles from root to immediate parent). The existing `task_ids` field SHALL continue to be returned for backward compatibility.

#### Scenario: Entry with linked tasks includes task details
- **WHEN** the timesheet GET response includes an entry with associated tasks
- **THEN** the entry object contains a `task_details` array with `id`, `title`, and `parent_titles` for each linked task

#### Scenario: Task with no parents has empty parent_titles
- **WHEN** a linked task is a top-level task (no parent)
- **THEN** its `parent_titles` array is empty

#### Scenario: Task with parents includes ancestor chain
- **WHEN** a linked task has a parent hierarchy (e.g., grandparent > parent > task)
- **THEN** its `parent_titles` array lists ancestor titles in order from root to immediate parent (e.g., `["grandparent", "parent"]`)

### Requirement: Entry rows display task names with hierarchy context
Time entry rows SHALL display the names of associated tasks. Each task name SHALL include a truncated breadcrumb prefix showing its parent hierarchy (e.g., "Parent > Task title"). When an entry has more than 3 associated tasks, the display SHALL show the first 3 task names followed by a "+N more" indicator.

#### Scenario: Entry row shows task names
- **WHEN** a time entry has associated tasks
- **THEN** the entry row displays the task names

#### Scenario: Task name includes parent breadcrumb
- **WHEN** a displayed task has parent tasks
- **THEN** the task name is shown with a breadcrumb prefix (e.g., "Parent > Task title")

#### Scenario: Many tasks show overflow indicator
- **WHEN** an entry has more than 3 associated tasks
- **THEN** the first 3 are shown followed by "+N more" where N is the count of remaining tasks
