## Context

People in the network/CRM currently have no user-driven categorization mechanism. The existing task `Tag` model serves a different domain with a different vocabulary. The network domain already has simple lookup-table models (`InteractionType`, `OrgType`, `InteractionMedium`) and uses `TypeaheadSelect` with inline creation throughout.

## Goals / Non-Goals

**Goals:**
- Add a `PersonTag` model with M2M to `Person`, fully separate from task tags
- Expose API endpoints for tag CRUD and people-list filtering by tag
- Integrate tag management into the person detail view using existing `TypeaheadSelect` pattern
- Show tags inline on each person row in the people list
- Support filtering the people list by one or more tags

**Non-Goals:**
- Sharing tags between tasks and people
- Tagging organizations (covered by `OrgType`)
- Tag colors, icons, hierarchy, or any metadata beyond name
- Tag-based filtering on other views (graph, interactions, relationships)

## Decisions

### 1. Separate PersonTag model (not reusing task Tag)

Task tags and person tags serve different vocabularies ("urgent", "bug" vs. "investor", "mentor"). Sharing would pollute both typeaheads and create confusing cross-domain queries. A separate model keeps both clean.

*Alternative considered*: Shared tag table with scoped M2M relationships. Rejected because the vocabularies are explicitly different and there's no identified cross-domain query need.

### 2. Model lives in `network/models/` alongside other network entities

Follows existing project structure. `PersonTag` is a network domain concept, not a task concept.

### 3. Same get_or_create pattern as task tags

Tags are auto-created on first use when adding to a person. This is the established pattern in `tasks/api/tags.py` and keeps the UX frictionless — no separate "manage tags" step.

### 4. API follows task tag endpoint pattern

- `GET /api/person-tags/` — list all (with optional `exclude_person` filter)
- `POST /api/people/{id}/tags/` — add tag (get_or_create by name)
- `DELETE /api/people/{id}/tags/{tag_id}/` — remove tag

This mirrors the task tag API structure, keeping the codebase consistent.

### 5. People list filtering via query parameter

`GET /api/people/?tag=investor` filters the list server-side. Multiple tags could be supported via repeated params (`?tag=investor&tag=mentor`) for AND filtering, but single-tag filtering is sufficient for v1.

### 6. Tags placed near top of person detail, above notes

Tags are a primary organizing mechanism and should have high visibility. Placement after contact fields (email, LinkedIn) and before notes.

### 7. Frontend uses existing TypeaheadSelect with onCreate

The `TypeaheadSelect` component already supports inline creation via `onCreate` callback — used for org types and interaction types. Person tags will follow the same pattern.

### 8. PersonSchema includes tags in response

Tags are included as an array in the person API response, avoiding extra API calls. The list endpoint annotation query joins the tag data.

## Risks / Trade-offs

- **Tag proliferation** → No mitigation needed for single-user app. User manages their own vocabulary.
- **Query performance on people list with tag filter** → Minimal risk with SQLite and small dataset. Standard M2M join.
- **Typeahead showing all person tags even irrelevant ones** → Acceptable for v1. The `exclude_person` param avoids showing already-assigned tags.
