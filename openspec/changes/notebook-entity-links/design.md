## Context

The notebook already tracks entity mentions via `PageEntityMention` records (entity_type + entity_id, indexed). The sidebar currently shows pages grouped by type (Recent wiki / Daily) with title-based search. Users want to filter pages by associated person or organization to quickly find relevant notes.

The existing `/api/notebook/mentions/{entity_type}/{entity_id}/` endpoint returns pages mentioning a specific entity — this is currently used by the `NotebookMentions` component on CRM detail pages.

## Goals / Non-Goals

**Goals:**
- Add entity-based filtering to the notebook page list API
- Add filter controls in the notebook sidebar to browse pages by person or org
- Reuse existing `PageEntityMention` data and indexes — no new models

**Non-Goals:**
- Changing how mentions are created or parsed
- Adding entity CRUD within the notebook UI
- Full-text search within page content (existing title search is separate)
- Tag-based or project-based filtering (can be added later with same pattern)

## Decisions

### 1. Backend: Add query params to existing page list endpoint

**Decision**: Extend `GET /api/notebook/pages/` with optional `entity_type` and `entity_id` query parameters rather than creating a new endpoint.

**Rationale**: The page list endpoint already supports `search` and `page_type` filters. Adding entity filters follows the same pattern and keeps the API surface small. The frontend already calls this endpoint for the sidebar — just needs to pass extra params.

**Alternative considered**: Using the existing `/api/notebook/mentions/{entity_type}/{entity_id}/` endpoint. Rejected because it returns `PageBacklink` (snippet-focused) rather than the full `PageListItem` shape the sidebar needs, and combining two different response shapes adds complexity.

### 2. Frontend: Dropdown filter in sidebar header

**Decision**: Add a filter dropdown in the sidebar above the page list. When an entity is selected, the page list shows only pages mentioning that entity. A clear button restores the unfiltered view.

**Rationale**: A dropdown filter is consistent with how filtering works elsewhere in the app (e.g., org type filter in network). It doesn't require a new view mode — the same page list just gets filtered.

**Alternative considered**: A separate "By Entity" tab/view in the sidebar. Rejected because it duplicates the page list UI and adds navigation complexity for a simple filter operation.

### 3. Entity selector: TypeaheadSelect component

**Decision**: Use the existing `TypeaheadSelect` component for entity selection, with people and organizations as options grouped by type.

**Rationale**: TypeaheadSelect already handles search, keyboard nav, and display. People and orgs are already loaded on mount for the mention autocomplete system.

## Risks / Trade-offs

- **[Performance with many mentions]** → The `PageEntityMention` table has an index on `(entity_type, entity_id)`, and we're joining to pages. For a single-user app with reasonable data volume, this is fine. If it becomes slow, a denormalized count column could help.
- **[Filter state persistence]** → Not persisting the filter in URL or localStorage. This is intentional — entity filtering is a quick lookup, not a persistent view. Users will typically filter, find their page, and clear.
