## Why

There's no quick-capture path for people and organizations from notebook notes. When jotting meeting notes or daily entries, you have to context-switch to the CRM to create a person or org record. This breaks writing flow and means contacts often go unrecorded. A Contacts Inbox — fed by notebook syntax — lets you capture names in the moment and triage them into proper CRM records later.

## What Changes

- Add a **ContactDraft model** — a lightweight staging record with just a name, quick notes, source page reference, and nullable FKs for promotion to Person or Organization. No required relational fields; those come at promotion time.
- Add **`@new[Name](notes)` syntax** in the notebook editor — on page save, this pattern creates a ContactDraft in the inbox. The parenthetical notes are optional. Content stays as-is until promotion.
- Add a **CRM Inbox tab** (first tab, before People) — lists pending ContactDraft records with triage actions: promote to Person, promote to Org, link to existing record, or dismiss. Promotion pre-fills a form (name split into first/last for people, quick notes into the notes field). When an existing Person or Org name-matches, a hint is surfaced.
- On **promotion or linking**, the notebook page content is rewritten: `@new[Name](notes)` → `@[person:ID|Name]` or `[[org:ID|Name]]`. Quick notes migrate into the promoted record's notes field. All pages containing the same `@new[Name]` are rewritten.

## Capabilities

### New Capabilities
- `contact-inbox`: ContactDraft model for staging quick-captured contacts, with promotion workflow to Person or Organization and dismiss action
- `contact-inbox-syntax`: `@new[Name](notes)` parser in notebook content that creates ContactDraft records on save

### Modified Capabilities
- `notebook-core`: Mention reconciliation extended to detect `@new[...]()` pattern and create ContactDraft records; page content rewrite on promotion
- `svelte-frontend`: CRM layout gains Inbox as first tab with triage UI (promote forms, match hints, dismiss)
- `django-api`: New ContactDraft CRUD endpoints, promote-to-person, promote-to-org, link-to-existing, and dismiss endpoints; match-hint endpoint for duplicate detection

## Non-goals

- Deduplication at capture time — writing `@new[Jane Smith]` twice creates two drafts; better to avoid interrupting notebook flow
- Bidirectional sync after promotion — once rewritten to `@[person:ID|Name]`, changes to the person's name don't propagate back to notebook content
- Auto-classification of person vs org at capture time — classification happens at triage
- Merging duplicate ContactDraft records — handle manually or in a future change
- Creating relationships or interactions from the inbox — triage produces a Person or Org record only

## Impact

- **Backend**: New `ContactDraft` model in `network/models/` with migration. New `@new[...]()` regex in `notebook/mentions.py` with draft creation logic. Promotion endpoint creates Person/Org, sets FK, rewrites all matching notebook pages. Match-hint query for existing Person/Org names.
- **Frontend**: CRM tab order changes to `Inbox | People | Orgs | Interactions | Leads`. New Inbox tab with draft list, triage buttons, promotion forms (pre-filled from draft), and match hints for existing records.
- **API**: New router in `network/api/` for ContactDraft CRUD + promote + dismiss + match-hints. Notebook save path extended in `reconcile_mentions`.
