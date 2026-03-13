## Why

Interactions and notebook pages are both key knowledge artifacts, but they exist in silos. When logging an interaction (e.g., a meeting with a client), users often have related notes on a notebook page — meeting prep, follow-up items, or detailed discussion notes. There's no way to connect them, forcing users to mentally track which pages relate to which interactions.

## What Changes

- Add a new `InteractionPage` join model linking interactions to notebook pages (many-to-many)
- Add API endpoints to manage interaction-page links from both directions
- Show linked notebook pages in the interaction detail panel (CRM side)
- Show linked interactions on notebook pages (notebook side)
- Extend the `PageEntityMention` system to support `interaction` as an entity type, enabling `[[interaction:ID|Label]]` syntax in notebook content

## Capabilities

### New Capabilities
- `interaction-note-links`: Backend model, API endpoints, and frontend UI for bidirectional linking between interactions and notebook pages

### Modified Capabilities
- `notebook-linking`: Add `interaction` as a supported `entity_type` in `PageEntityMention`, enabling `[[interaction:ID|Label]]` mention syntax in notebook content

## Impact

- **Backend**: New `InteractionPage` model in `network/models/task_links.py`, new API endpoints in `network/api/`, migration, mention parser update in `notebook/mentions.py`
- **Frontend**: Interaction detail panel gains "Linked Notes" section; notebook page gains "Linked Interactions" section or shows interaction backlinks; API client updated with new endpoints
- **Existing behavior**: No breaking changes — existing interaction and notebook features remain unchanged

## Non-goals

- Auto-linking interactions to pages based on date or content matching
- Inline interaction creation from notebook pages
- Changing the interaction model itself (no new fields on Interaction)
