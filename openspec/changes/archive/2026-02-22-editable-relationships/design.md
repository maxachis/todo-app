## Context

The Relationships page (`frontend/src/routes/relationships/+page.svelte`) displays person-to-person and organization-to-person relationships in two panels. Each panel has a create form and a list of existing relationships showing linked entities and notes. Users can create and delete relationships but cannot edit them.

The backend already exposes PUT endpoints (`/relationships/people/{id}/` and `/relationships/organizations/{id}/`) that accept a `notes` field. The frontend API client (`frontend/src/lib/api/index.ts`) has `getAll`, `create`, and `remove` methods but no `update` method.

## Goals / Non-Goals

**Goals:**
- Allow users to edit the notes on existing relationships directly in the Relationships page
- Add `update` API client methods that call the existing backend PUT endpoints
- Keep the interaction simple — inline editing with minimal UI overhead

**Non-Goals:**
- Changing which people/organizations are linked (reassigning endpoints)
- Editing relationships from other pages (People, Organizations, Interactions)
- Backend changes (endpoints already exist)

## Decisions

### Inline edit via click on notes area
**Decision:** Clicking a relationship item's notes text (or an "Edit" button if no notes exist) switches the notes area to a `<textarea>` for editing. Blur or Enter saves; Escape cancels.

**Rationale:** This follows the same inline-edit pattern used for list names and section titles elsewhere in the app (double-click to edit, blur to save). A modal or separate form would be heavier than needed for a single text field. Using single-click (rather than double-click) since the notes area is not otherwise interactive.

**Alternatives considered:**
- Modal dialog — too heavy for editing one text field
- Always-visible textarea — clutters the list view with edit controls on every item

### API client update methods
**Decision:** Add `api.relationships.people.update(id, payload)` and `api.relationships.organizations.update(id, payload)` that issue PUT requests to the existing endpoints.

**Rationale:** Mirrors the existing pattern for other entity updates (e.g., `api.people.update`, `api.organizations.update`). Payload type is `{ notes?: string }`.

## Risks / Trade-offs

- [Minimal risk] The change is small and frontend-only — no data model or migration involved.
- [UX trade-off] Single-click to edit may conflict with future click-to-select behavior if a detail panel is added to the Relationships page → Acceptable for now since no detail panel is planned.
