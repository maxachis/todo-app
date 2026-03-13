## Why

Notebook pages accumulate mentions of people and organizations through `@[person:ID|Name]` and `[[org:ID|Name]]` syntax, but there's no way to browse or filter notes by associated entity. Users can see which pages mention a specific person (via the NotebookMentions component on detail pages), but cannot navigate the notebook itself organized around people or orgs — e.g., "show me all my notes about Acme Corp" or "what have I written about John?"

## What Changes

- Add a filter/browse mode to the notebook sidebar that groups or filters pages by associated person or organization
- Surface entity associations prominently in the notebook UI so users can quickly find related notes
- Leverage the existing `PageEntityMention` data — no new linking model needed

## Capabilities

### New Capabilities
- `notebook-entity-filter`: Filter and browse notebook pages by associated people or organizations. Adds entity-based filtering controls to the notebook sidebar.

### Modified Capabilities
- `notebook-frontend`: UI changes to the notebook page to support entity filtering in the sidebar

## Impact

- **Frontend**: `frontend/src/routes/notebook/+page.svelte` — sidebar gets entity filter controls
- **Backend**: `notebook/api/pages.py` — may need query params for filtering pages by entity type/ID
- **API types**: `frontend/src/lib/api/` — new filter parameters on page list endpoint
- No database migrations needed — `PageEntityMention` already indexes `(entity_type, entity_id)`

## Non-goals

- Creating new linking mechanisms between pages and entities (existing mentions are sufficient)
- Changing how mentions are created or parsed
- Adding entity management within the notebook (that stays in CRM/Network)
