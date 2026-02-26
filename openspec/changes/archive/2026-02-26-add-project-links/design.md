## Context

Projects currently store only `name`, `description`, `is_active`, and `position`. Users need a way to attach external resource URLs (GitHub repos, design docs, deployed apps, etc.) with short descriptive labels. The codebase already has patterns for nested link resources (see `TaskPerson`, `TaskOrganization` in `network/models/task_links.py`) and nested CRUD endpoints (see `network/api/task_links.py`).

## Goals / Non-Goals

**Goals:**
- Allow users to attach multiple URL links with short descriptor labels to any project
- Provide dedicated CRUD API endpoints nested under the project resource
- Display links as clickable anchors on the project card UI, with inline add/edit/remove

**Non-Goals:**
- URL reachability validation or link preview fetching
- Link ordering/reordering (append-only display order by creation)
- Favicon or Open Graph metadata extraction
- Link deduplication enforcement (same URL can appear twice with different descriptors)

## Decisions

### 1. Separate `ProjectLink` model (not JSONField)

Use a dedicated Django model with a ForeignKey to `Project`, consistent with existing link patterns (`TaskPerson`, `TaskOrganization`).

**Why over JSONField:** Queryable, standard Django admin support, easier to extend later, consistent with codebase conventions. The one-to-many FK pattern is already established.

### 2. Nested REST endpoints under `/projects/{id}/links/`

Follow the existing pattern from `network/api/task_links.py` — dedicated router with list/create/update/delete endpoints nested under the parent resource.

**Routes:**
- `GET /projects/{project_id}/links/` — list links for a project
- `POST /projects/{project_id}/links/` — create a link
- `PUT /projects/{project_id}/links/{link_id}/` — update a link
- `DELETE /projects/{project_id}/links/{link_id}/` — delete a link

**Why over inline on project CRUD:** Simpler per-link operations, avoids complex diff logic on project update, consistent with how task links work.

### 3. Model fields: `url` (CharField 2000) + `descriptor` (CharField 100)

- `url`: CharField with max_length=2000, required, stripped on save
- `descriptor`: CharField with max_length=100, required, stripped on save — short label like "GitHub Repo", "Figma", "Production"
- `project`: ForeignKey to Project, CASCADE on delete
- `created_at`: auto timestamp

**Why CharField over URLField:** URLField just adds URL validation to CharField; we want to keep it simple per the non-goals (no validation beyond non-empty).

### 4. Frontend: inline link list on project card with add/remove

Links displayed as a list of clickable `<a>` tags below the project description on each card. An inline form with two inputs (descriptor + URL) for adding new links. Edit and delete via small icon buttons per link row. Follows the same inline-editing pattern already used for project name/description.

### 5. Include links in project list response

Eagerly load links via `prefetch_related("links")` in the project queryset and include them as a nested array in `ProjectSchema`. This avoids N+1 queries and extra API calls on page load.

## Risks / Trade-offs

- **No URL validation** → Users can save malformed URLs. Mitigation: acceptable per non-goals; the descriptor provides context even if URL is wrong.
- **No ordering** → Links appear in creation order only. Mitigation: simple and predictable; can add drag-and-drop later if needed.
- **Extra prefetch on project list** → Slight overhead. Mitigation: negligible for a single-user app with few projects.
