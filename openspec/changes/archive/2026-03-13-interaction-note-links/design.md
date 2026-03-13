## Context

Interactions (CRM) and notebook pages are separate features with no cross-references. The system already has established patterns for entity linking:

1. **Explicit join tables**: `TaskPersonLink`, `TaskOrganizationLink`, `InteractionTaskLink` in `network/models/task_links.py` — used for structured links managed via dedicated API endpoints and the `LinkedEntities` UI component.
2. **Content-based mentions**: `PageEntityMention` in `notebook/models.py` — auto-parsed from page content using `@[person:ID|Name]` and `[[type:ID|Label]]` syntax, reconciled on save.

Both paradigms should be used: explicit links for the interaction detail panel, and content-based mentions for the notebook editor.

## Goals / Non-Goals

**Goals:**
- Allow users to link notebook pages to interactions from the interaction detail panel
- Allow users to mention interactions in notebook content using `[[interaction:ID|Label]]` syntax
- Show linked interactions on notebook pages (via entity backlinks API)
- Follow existing patterns for both linking paradigms

**Non-Goals:**
- Auto-linking based on dates or content similarity
- Creating interactions from within the notebook
- Full-text search across interactions from notebook
- Inline interaction previews in notebook content

## Decisions

### 1. Use an explicit join table for interaction-page links

**Choice**: New `InteractionPageLink` model in `network/models/task_links.py` with `interaction` FK and `page` FK, following the same pattern as `InteractionTaskLink`.

**Alternative considered**: Rely solely on `PageEntityMention` (content-based). Rejected because content-based mentions only work from notebook → interaction direction. We need linking from the interaction detail panel too, where the user picks a page from a list — not by editing content.

**Alternative considered**: Single generic link table with content-type-like polymorphism. Rejected — the existing codebase uses explicit typed join tables throughout and this is simpler.

### 2. Extend PageEntityMention to support `interaction` entity type

**Choice**: Add `"interaction"` to the `entity_type` choices in `PageEntityMention` and update the mention parser regex in `notebook/mentions.py` to recognize `[[interaction:ID|Label]]`.

**Rationale**: This follows the exact pattern already used for `task`, `org`, `project`, and `person` mentions. The entity backlinks API (`GET /notebook/mentions/{type}/{id}/`) already works generically — adding `interaction` as a type requires no new endpoints.

### 3. Reuse LinkedEntities component for both directions

**Choice**: On the interaction detail panel, add a "Linked Notes" section using the existing `LinkedEntities` component pattern. On notebook pages, show interaction backlinks using the existing entity backlinks mechanism (already supported by `GET /notebook/mentions/{type}/{id}/`).

**Rationale**: Both UI patterns already exist. The interaction detail page already uses `LinkedEntities` for task links. The notebook page already displays backlinks for page-to-page links.

### 4. API endpoint structure

**Choice**: Follow the nested resource pattern used by task links:
- `GET/POST /api/interactions/{id}/pages/` — list/add linked pages
- `DELETE /api/interactions/{id}/pages/{page_id}/` — remove link
- `GET /api/notebook/pages/{slug}/interactions/` — list interactions linked to a page

The reverse direction (page → interactions) uses a dedicated endpoint rather than the mention backlinks API, because explicit links and content mentions are separate concerns.

## Risks / Trade-offs

- **Dual linking mechanisms**: An interaction can be linked to a page both explicitly (via join table) and implicitly (via `[[interaction:ID|Label]]` in content). This is consistent with how tasks work (tasks have explicit links AND can be mentioned in pages), so users already have this mental model. The UI should show both sources.
  → Mitigation: The page-side "Linked Interactions" section queries both the explicit link table and the entity mentions, deduplicating by interaction ID.

- **Interaction label for mentions**: The `[[interaction:ID|Label]]` syntax needs a display label. Interactions don't have a title field — they're identified by type + date + people.
  → Mitigation: Use a computed label like "Meeting with John Smith (2026-03-13)" derived from interaction type, first person, and date.
