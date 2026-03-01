## Why

Notes and context currently live outside the app — in separate note-taking tools, documents, or memory. When logging an interaction or working on a task, the background context (meeting notes, daily observations, ideas) has to be mentally translated from one medium into structured fields. A notebook integrated into Nexus eliminates that friction: write freeform, tag the people/orgs/tasks/projects you mention inline, and let the system build the connections automatically. Entity detail views gain a "mentioned in" backlinks section, turning the app into a lightweight personal knowledge base.

## What Changes

- Add a **Notebook** top-level nav tab with a two-panel layout: page sidebar (left) + editor (right)
- Two page types: **daily** (one per date, created on demand via a "Today" button) and **wiki** (freeform titled pages)
- Editor is a plain textarea with two typeahead triggers:
  - `@` triggers a people-only typeahead (inserts `@[person:ID|Name]`)
  - `[[` triggers a typeahead across pages, tasks, orgs, and projects (inserts `[[type:ID|Title]]`)
- Content is stored as markdown with the mention syntax above; entity references are extracted on save into join tables
- **Bidirectional page links**: when Page A references `[[page:B|...]]`, Page B's backlinks section shows Page A
- **Entity backlinks**: person, org, task, and project detail views gain a "Notebook Mentions" section listing pages that reference them
- Auto-save on blur or after a debounced typing pause
- Backend: new `Page` model, `PageEntityMention` join table, `PageLink` join table, CRUD API, and backlinks query endpoints

## Non-goals

- Full-text search across notebook content
- Rich text / WYSIWYG editing or live markdown preview/rendering
- Tags, folders, or hierarchical page organization
- Nested/child pages
- File attachments or image embedding
- Collaborative editing or sharing
- Mobile-specific layout optimizations

## Capabilities

### New Capabilities
- `notebook-core`: Page model (daily + wiki types), CRUD API, slug-based URLs, auto-save, mention syntax parsing, entity reference extraction on save
- `notebook-frontend`: Two-panel notebook route with page sidebar, textarea editor, `@` people typeahead, `[[` entity typeahead, "Today" daily page button
- `notebook-linking`: Bidirectional page-to-page links via PageLink join table, entity mentions via PageEntityMention join table, backlinks display on notebook pages and entity detail views

### Modified Capabilities
- `network-frontend`: Person, organization detail views gain a "Notebook Mentions" backlinks section
- `svelte-frontend`: Navigation updated with Notebook tab; task and project detail views gain a "Notebook Mentions" backlinks section

## Impact

- **Backend**: New `notebook/` Django app with `Page`, `PageEntityMention`, `PageLink` models; Django Ninja API routers for CRUD, backlinks; mention-parsing utility; migrations
- **Frontend**: New `/notebook` route with two-panel layout; new `NotebookEditor` component with textarea + typeahead; new `BacklinksSection` shared component; sidebar with page list, "Today" button, "New Page" button
- **API types**: New TypeScript types for Page, PageEntityMention, PageLink, create/update inputs
- **Entity detail views**: People, orgs, task detail, and project detail views updated to show notebook backlinks
- **Navigation**: New "Notebook" tab added to `+layout.svelte`
- **Dependencies**: No new dependencies expected (typeahead pattern already exists via TypeaheadSelect)
