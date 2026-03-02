# Contact Inbox Syntax

## Purpose

Notebook syntax for quick-capturing contacts via `@new[Name](notes)` patterns and the rewrite logic that converts them to proper entity mentions upon promotion.

## Requirements

### Requirement: `@new[Name](notes)` syntax creates contact drafts on save
The system SHALL detect the pattern `@new[Name](notes)` in notebook page content during the save flow (within `reconcile_mentions`). The parenthetical notes portion is optional — `@new[Name]` is also valid. For each match where no ContactDraft with the same `name` and `source_page` already exists, the system SHALL create a ContactDraft with the extracted name, notes, and source page. The page content SHALL NOT be rewritten at capture time — the `@new[...]` text remains in the content until promotion.

#### Scenario: Single @new creates a draft
- **WHEN** a page is saved with content containing `@new[Jane Smith](works at Stripe)`
- **THEN** a ContactDraft is created with `name="Jane Smith"`, `quick_notes="works at Stripe"`, `source_page` set to the page

#### Scenario: @new without parenthetical creates draft with empty notes
- **WHEN** a page is saved with content containing `@new[Bob Chen]`
- **THEN** a ContactDraft is created with `name="Bob Chen"`, `quick_notes=""`, `source_page` set to the page

#### Scenario: Multiple @new patterns create multiple drafts
- **WHEN** a page is saved with content containing `@new[Jane Smith](works at Stripe)` and `@new[Acme Corp](partner)`
- **THEN** two ContactDraft records are created, one for each name

#### Scenario: Duplicate @new on same page is idempotent
- **WHEN** a page containing `@new[Jane Smith](notes)` is saved, and a ContactDraft with `name="Jane Smith"` and `source_page` equal to this page already exists
- **THEN** no new draft is created (the existing draft is preserved)

#### Scenario: Same name on different pages creates separate drafts
- **WHEN** page A is saved with `@new[Jane Smith](context A)` and page B is saved with `@new[Jane Smith](context B)`
- **THEN** two separate ContactDraft records are created, one per page

#### Scenario: Content is not rewritten at capture
- **WHEN** a page is saved with `@new[Jane Smith](notes)`
- **THEN** the page content still contains `@new[Jane Smith](notes)` after save — no rewrite occurs

### Requirement: Notebook content rewrite on promotion
When a ContactDraft is promoted to a Person or Organization (or linked to an existing one), the system SHALL rewrite all notebook page content containing `@new[Name]` (with optional parenthetical notes) to the appropriate mention syntax. For Person promotion: `@new[Name](...)` → `@[person:ID|Name]`. For Organization promotion: `@new[Name](...)` → `[[org:ID|Name]]`. The rewrite SHALL apply across ALL pages, not just the draft's `source_page`.

#### Scenario: Rewrite to person mention on promotion
- **WHEN** a ContactDraft with `name="Jane Smith"` is promoted to Person #42
- **THEN** all pages containing `@new[Jane Smith](...)` or `@new[Jane Smith]` are rewritten to `@[person:42|Jane Smith]`

#### Scenario: Rewrite to org mention on promotion
- **WHEN** a ContactDraft with `name="Acme Corp"` is promoted to Organization #5
- **THEN** all pages containing `@new[Acme Corp](...)` or `@new[Acme Corp]` are rewritten to `[[org:5|Acme Corp]]`

#### Scenario: Rewrite spans multiple pages
- **WHEN** `@new[Jane Smith]` appears on page A, page B, and page C, and the draft is promoted to Person #42
- **THEN** all three pages are rewritten to contain `@[person:42|Jane Smith]`

#### Scenario: Parenthetical notes are stripped on rewrite
- **WHEN** a page contains `@new[Jane Smith](works at Stripe, met at conf)` and the draft is promoted
- **THEN** the page content becomes `@[person:42|Jane Smith]` — the parenthetical notes are removed (they migrated to the Person's notes field)
