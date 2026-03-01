## Context

Nexus currently has structured entity models (people, organizations, tasks, projects, interactions) with a typed API and SvelteKit frontend. Notes exist only as `notes` text fields on individual entities. There is no freeform writing surface. Users capture context in external tools (Obsidian, documents, etc.) and manually translate relevant bits into Nexus's structured fields.

The frontend uses a two-panel layout pattern on entity routes (list sidebar + detail), TypeaheadSelect for entity selection with typeahead filtering, and a block-based MarkdownEditor for task/interaction notes. The backend follows Django model + Django Ninja API router conventions with typed schemas.

## Goals / Non-Goals

**Goals:**
- Add a freeform notebook with daily journal pages and wiki pages
- Support inline `@` mentions for people and `[[]]` mentions for pages, tasks, orgs, and projects
- Extract entity references on save into join tables for backlink queries
- Support bidirectional page-to-page linking
- Display backlinks on notebook pages and on existing entity detail views
- Auto-save content on blur or debounced typing pause

**Non-Goals:**
- Full-text search across notebook content
- Rich text / WYSIWYG editing or live markdown preview
- Tags, folders, or hierarchical page organization
- File attachments or image embedding
- Collaborative editing

## Decisions

### 1. App placement: new Django app vs extend existing

**Decision**: Create a new `notebook/` Django app alongside `tasks/` and `network/`.

**Alternatives considered**:
- Add models to `network/` — notebook isn't network-specific, it references tasks and projects too
- Add to `tasks/` — same problem, notebook is cross-cutting

**Rationale**: The notebook is a new domain that references entities from both `tasks` and `network`. A separate app keeps concerns clean and follows the existing pattern of one app per domain.

### 2. Mention syntax: custom symbols vs standard conventions

**Decision**: Use `@[person:ID|Display Name]` for people and `[[type:ID|Display Name]]` for everything else (pages, tasks, orgs, projects).

**Alternatives considered**:
- Different single-character prefixes per type (`@`, `!`, `$`, `#`) — collision risk with normal punctuation (`!` and `$` appear in regular prose)
- Uniform `@` for all types — noisier typeahead results, harder to distinguish
- Typed bracket syntax for everything — loses the natural `@person` convention

**Rationale**: `@` for people is universal convention. `[[]]` is established wiki syntax (Obsidian, Notion, Logseq), essentially impossible to trigger accidentally, and naturally extends to page-to-page linking. The `type:ID|label` internal format keeps the raw markdown human-readable even outside the app.

### 3. Editor approach: textarea vs rich text vs split pane

**Decision**: Plain textarea with floating typeahead dropdowns. No markdown rendering or preview.

**Alternatives considered**:
- TipTap/ProseMirror WYSIWYG — rich experience but large dependency and significant complexity
- Split-pane (edit + preview) — more visual but doubles the screen space needed
- Extend existing MarkdownEditor — its click-to-edit-block pattern doesn't suit continuous writing

**Rationale**: Entries are expected to be short (a few paragraphs). A plain textarea is the fastest to build, has zero dependencies, and provides a distraction-free writing experience. The typeahead overlay pattern is proven (TypeaheadSelect already exists). Rendering/preview can be added later if needed.

### 4. Entity reference storage: inline-only vs extracted join tables

**Decision**: Store references in both the content (inline syntax) and extracted join tables (`PageEntityMention`, `PageLink`). On each save, parse the content and reconcile the join tables.

**Alternatives considered**:
- Inline-only (parse on read) — no join tables, but makes backlink queries expensive (full-text scan of all pages)
- Join-tables-only (no inline syntax) — loses the readable markdown and breaks if content is edited externally

**Rationale**: The dual storage is necessary for efficient backlink queries while keeping the content self-describing. The reconciliation on save is cheap for short documents. The join tables are the source of truth for queries; the inline syntax is the source of truth for what the user wrote.

### 5. Page slug generation

**Decision**: Auto-generate slugs from title on create, allow manual override. Daily pages use the date as slug (e.g., `2026-02-28`). Slugs must be unique.

**Alternatives considered**:
- ID-only URLs (`/notebook/42`) — not human-readable
- Title-only URLs (no slug field) — titles can change, breaking bookmarks

**Rationale**: Slugs provide readable URLs. Auto-generation from title covers the common case. The slug is set at creation time and doesn't change when the title is edited (avoiding broken links). Daily page slugs are deterministic from the date.

### 6. Typeahead data source: dedicated search endpoint vs reuse existing list endpoints

**Decision**: Reuse existing list endpoints (`/api/people/`, `/api/organizations/`, `/api/tasks/`, `/api/projects/`) for typeahead data, fetched on component mount. Add a dedicated `GET /api/notebook/pages/?search=` for page search in the `[[` typeahead.

**Alternatives considered**:
- Unified search endpoint that queries all entity types — more work to build, single point of failure
- Fetch on every keystroke — unnecessary load for a single-user app with modest data

**Rationale**: The existing entity list endpoints already return the data needed (id + name/title). For a single-user app, caching all entities client-side on mount is fine. Only page search needs a dedicated endpoint since pages are a new entity type.

### 7. Backlinks on entity detail views: inline vs separate section

**Decision**: Add a "Notebook Mentions" collapsible section to entity detail views (people, orgs, task detail, project detail), showing pages that mention the entity with title, date, and a content snippet.

**Alternatives considered**:
- Inline badges/links in the entity header — too noisy for entities with many mentions
- Separate "Mentions" tab — over-engineering for what's likely a short list

**Rationale**: A collapsible section follows the existing pattern for related data on detail views (e.g., Linked People & Orgs on tasks). It's visible but not intrusive.

## Risks / Trade-offs

- **[Complexity] Mention parsing on every save** → For short documents (a few paragraphs), regex parsing is negligible. If pages grow large, could debounce or defer parsing. The reconciliation (diff current mentions vs stored mentions) is bounded by the number of mentions per page, not page length.

- **[UX] Raw mention syntax visible in textarea** → Users see `@[person:7|John Smith]` while editing instead of just "John Smith". This is the tradeoff of the plain textarea approach. Mitigated by: the syntax is inserted by typeahead (users don't type it manually), and it's readable enough. Can layer rendering on top later.

- **[Data integrity] Stale mentions after entity deletion** → If a person or task is deleted, their mentions remain in page content as broken references. Mitigated by: the join table entries can be cleaned up via CASCADE, and a future enhancement could flag or clean broken inline references.

- **[Scope] Cross-app model references** → The `PageEntityMention` table references entities from both `tasks` and `network` apps via `entity_type` + `entity_id` (generic foreign key pattern). This avoids hard FK dependencies across apps but means no database-level referential integrity for mentions. Acceptable for a mentions/backlinks feature where broken references are non-critical.

## Open Questions

None — all major decisions resolved during exploration.
