## MODIFIED Requirements

### Requirement: Mention parsing extracts entity references on save
The system SHALL parse page content on every create and update to extract entity references. The parser SHALL recognize two patterns: `@[person:ID|Label]` for people and `[[type:ID|Label]]` for pages, tasks, organizations, and projects (where type is one of `page`, `task`, `org`, `project`). Additionally, the parser SHALL detect unchecked checkbox lines matching `- [ ] <text>` where `<text>` does not contain `[[task:` — for each, it SHALL create a task in the system Inbox section and rewrite the line to `- [ ] [[task:ID|Title]]`. **The parser SHALL also detect `@new[Name](optional notes)` patterns and create ContactDraft records for each new occurrence (where no draft with the same name and source page exists).** After all checkbox and contact-draft processing, the system SHALL reconcile the `PageEntityMention` and `PageLink` join tables — adding new references, removing stale ones — so the tables always reflect the current content.

#### Scenario: @new pattern creates contact draft during save
- **WHEN** a page is saved with content `"Had coffee with @new[Jane Smith](works at Stripe)"`
- **THEN** the system creates a ContactDraft with `name="Jane Smith"`, `quick_notes="works at Stripe"`, and `source_page` set to this page, and the page content is NOT rewritten

#### Scenario: @new and checkbox patterns coexist
- **WHEN** a page is saved with content containing both `- [ ] Follow up with Jane` and `@new[Jane Smith](Stripe)`
- **THEN** a task is created from the checkbox line (content rewritten), a ContactDraft is created from the @new pattern (content NOT rewritten), and mention reconciliation runs on the final content
