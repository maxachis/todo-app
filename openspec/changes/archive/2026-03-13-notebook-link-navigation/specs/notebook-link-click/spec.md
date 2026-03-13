## ADDED Requirements

### Requirement: Ctrl+Click navigates to referenced entity

The notebook editor SHALL support Ctrl+Click (Cmd+Click on macOS) on rendered mention chips to navigate to the referenced entity. The editor MUST detect the modifier key and the target chip, extract the entity type and identifier, and perform in-app navigation.

#### Scenario: Ctrl+Click on a page mention chip
- **WHEN** the user Ctrl+Clicks (or Cmd+Clicks on macOS) on a `[[page:ID|Label]]` mention chip
- **THEN** the notebook navigates to that page using the page's slug (equivalent to clicking the page in the sidebar)

#### Scenario: Ctrl+Click on a person mention chip
- **WHEN** the user Ctrl+Clicks on a `@[person:ID|Label]` mention chip
- **THEN** the app navigates to `/crm/people` with the person selected

#### Scenario: Ctrl+Click on a task mention chip
- **WHEN** the user Ctrl+Clicks on a `[[task:ID|Label]]` mention chip
- **THEN** the app navigates to the Tasks route with the task selected

#### Scenario: Ctrl+Click on an organization mention chip
- **WHEN** the user Ctrl+Clicks on a `[[org:ID|Label]]` mention chip
- **THEN** the app navigates to `/crm/orgs` with the organization selected

#### Scenario: Ctrl+Click on a project mention chip
- **WHEN** the user Ctrl+Clicks on a `[[project:ID|Label]]` mention chip
- **THEN** the app navigates to `/projects` with the project selected

#### Scenario: Plain click on a mention chip does not navigate
- **WHEN** the user clicks a mention chip without holding Ctrl/Cmd
- **THEN** the editor positions the cursor as normal and no navigation occurs

### Requirement: Visual cursor affordance on Ctrl/Cmd hover

When the Ctrl key (Cmd on macOS) is held down, mention chips in the editor SHALL display a pointer cursor and underline styling to indicate they are clickable.

#### Scenario: Ctrl held shows pointer cursor on chips
- **WHEN** the user presses and holds Ctrl (or Cmd on macOS) while the mouse is over the notebook editor
- **THEN** all mention chips display `cursor: pointer` and underlined label text

#### Scenario: Releasing Ctrl restores default cursor
- **WHEN** the user releases the Ctrl/Cmd key
- **THEN** mention chips return to their default cursor and styling

### Requirement: Navigation uses data attributes on chip DOM elements

Mention chip DOM elements SHALL include `data-entity-type` and `data-entity-id` attributes to support click-based navigation. Page mention chips SHALL additionally include a `data-entity-slug` attribute.

#### Scenario: Mention chip DOM has data attributes
- **WHEN** a mention chip is rendered for `[[task:42|Fix bug]]`
- **THEN** the chip's DOM element has `data-entity-type="task"` and `data-entity-id="42"`

#### Scenario: Page mention chip includes slug
- **WHEN** a mention chip is rendered for `[[page:7|Meeting Notes]]` and the page has slug `meeting-notes`
- **THEN** the chip's DOM element has `data-entity-type="page"`, `data-entity-id="7"`, and `data-entity-slug="meeting-notes"`
