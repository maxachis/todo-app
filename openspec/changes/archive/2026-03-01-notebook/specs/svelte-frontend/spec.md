## MODIFIED Requirements

### Requirement: Navigation includes Notebook tab
The top navigation bar SHALL include a "Notebook" tab linking to `/notebook`, placed after "Graph" in the tab order. The tab SHALL be highlighted when the user is on any `/notebook` route.

#### Scenario: User sees Notebook tab
- **WHEN** the user views any page
- **THEN** the top navigation bar displays a "Notebook" tab

#### Scenario: Notebook tab is highlighted on notebook routes
- **WHEN** the user is on `/notebook` or `/notebook/some-page`
- **THEN** the "Notebook" tab is highlighted in the navigation bar

### Requirement: Task detail panel includes notebook mentions
The task detail panel SHALL include a collapsible "Notebook Mentions" section showing pages that mention the selected task. The section SHALL fetch data from `GET /api/notebook/mentions/task/{id}/` and display each entry as a clickable row with page title, type badge, and content snippet. Clicking an entry SHALL navigate to `/notebook/{slug}`. The section SHALL be hidden when there are no mentions.

#### Scenario: Task with notebook mentions
- **WHEN** the user views a task that is mentioned in 2 notebook pages
- **THEN** a "Notebook Mentions" section displays with 2 entries

#### Scenario: Task with no notebook mentions
- **WHEN** the user views a task with no notebook mentions
- **THEN** the "Notebook Mentions" section is not displayed

### Requirement: Project detail view includes notebook mentions
The project page SHALL include a collapsible "Notebook Mentions" section on project cards for projects that are mentioned in notebook pages. The section SHALL fetch data from `GET /api/notebook/mentions/project/{id}/` and display entries as clickable rows.

#### Scenario: Project with notebook mentions
- **WHEN** a project is mentioned in notebook pages
- **THEN** the project card displays a "Notebook Mentions" section with clickable entries

#### Scenario: Project with no notebook mentions
- **WHEN** a project has no notebook mentions
- **THEN** no "Notebook Mentions" section is shown on the project card
