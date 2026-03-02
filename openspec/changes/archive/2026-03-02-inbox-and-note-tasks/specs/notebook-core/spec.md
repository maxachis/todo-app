## MODIFIED Requirements

### Requirement: Mention parsing extracts entity references on save
The system SHALL parse page content on every create and update to extract entity references. The parser SHALL recognize two patterns: `@[person:ID|Label]` for people and `[[type:ID|Label]]` for pages, tasks, organizations, and projects (where type is one of `page`, `task`, `org`, `project`). Additionally, the parser SHALL detect unchecked checkbox lines matching `- [ ] <text>` where `<text>` does not contain `[[task:` — for each, it SHALL create a task in the system Inbox section and rewrite the line to `- [ ] [[task:ID|Title]]`. After all checkbox processing, the system SHALL reconcile the `PageEntityMention` and `PageLink` join tables — adding new references, removing stale ones — so the tables always reflect the current content.

#### Scenario: Content with people and task mentions
- **WHEN** a page is saved with content `"Met with @[person:7|John Smith] about [[task:189|Deploy fix]]"`
- **THEN** the system creates a `PageEntityMention` for (page, person, 7) and (page, task, 189)

#### Scenario: Content with page link
- **WHEN** a page is saved with content `"See [[page:12|Migration Runbook]] for details"`
- **THEN** the system creates a `PageLink` from this page to page 12

#### Scenario: Mention removed from content
- **WHEN** a page previously mentioned person 7 and is updated with content that no longer contains `@[person:7|...]`
- **THEN** the `PageEntityMention` for (page, person, 7) is deleted

#### Scenario: Content with no mentions
- **WHEN** a page is saved with content containing no mention syntax
- **THEN** no `PageEntityMention` or `PageLink` records are created (or existing ones are cleared)

#### Scenario: Duplicate mentions in content
- **WHEN** a page mentions `@[person:7|John Smith]` twice in the content
- **THEN** only one `PageEntityMention` record exists for (page, person, 7)

#### Scenario: Checkbox line creates task and rewrites content
- **WHEN** a page is saved with content containing `- [ ] Review contract`
- **THEN** a task titled "Review contract" is created in the Inbox section, the line is rewritten to `- [ ] [[task:ID|Review contract]]`, and a `PageEntityMention` for (page, task, ID) is created
