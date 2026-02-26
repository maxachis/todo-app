## 1. Backend Model & Migration

- [x] 1.1 Add `ProjectLink` model to `tasks/models.py` with fields: `project` (FK to Project, CASCADE), `url` (CharField max 2000), `descriptor` (CharField max 100), `created_at` (auto_now_add). Meta: ordering by `created_at`.
- [x] 1.2 Run `makemigrations` and `migrate` to create the `tasks_projectlink` table

## 2. Backend API Schemas

- [x] 2.1 Add `ProjectLinkSchema` to `tasks/api/schemas.py` (id, project_id, url, descriptor, created_at)
- [x] 2.2 Add `ProjectLinkCreateInput` schema (url: str, descriptor: str)
- [x] 2.3 Add `ProjectLinkUpdateInput` schema (url: str | None, descriptor: str | None)
- [x] 2.4 Add `links: list[ProjectLinkSchema] = []` field to `ProjectSchema`

## 3. Backend API Endpoints

- [x] 3.1 Create `tasks/api/project_links.py` with a new Router for project link CRUD
- [x] 3.2 Implement `GET /projects/{project_id}/links/` — list links ordered by created_at
- [x] 3.3 Implement `POST /projects/{project_id}/links/` — create link with strip + non-empty validation, return 201
- [x] 3.4 Implement `PUT /projects/{project_id}/links/{link_id}/` — update link fields with strip + non-empty validation
- [x] 3.5 Implement `DELETE /projects/{project_id}/links/{link_id}/` — delete link, return 204
- [x] 3.6 Update `_project_queryset()` in `tasks/api/projects.py` to `prefetch_related("links")`
- [x] 3.7 Update `_serialize_project()` to include `links` array from prefetched data
- [x] 3.8 Register the project_links router in the Django Ninja API setup

## 4. Backend Tests

- [x] 4.1 Add API tests for project link CRUD in `tasks/tests/test_api_projects.py` (or new test file): list, create, create-with-blank-url, create-with-blank-descriptor, update, update-with-blank-url, delete, delete-nonexistent, cascade-on-project-delete
- [x] 4.2 Verify project list response includes `links` array

## 5. Frontend Types & API Client

- [x] 5.1 Add `ProjectLink` interface to `frontend/src/lib/api/types.ts` (id, project_id, url, descriptor, created_at)
- [x] 5.2 Add `links: ProjectLink[]` to the `Project` interface
- [x] 5.3 Add `projectLinks` methods to `frontend/src/lib/api/index.ts`: list, create, update, remove (nested under `/projects/{id}/links/`)

## 6. Frontend Store

- [x] 6.1 Update `frontend/src/lib/stores/projects.ts` to handle `links` on project objects (comes from API response; no separate fetch needed)
- [x] 6.2 Add `createProjectLink`, `updateProjectLink`, `deleteProjectLink` async functions to the store with optimistic UI updates

## 7. Frontend UI

- [x] 7.1 Update project card in `frontend/src/routes/projects/+page.svelte` to display links as clickable anchors (descriptor as text, url as href, target="_blank", rel="noopener noreferrer")
- [x] 7.2 Add "Add link" button that reveals an inline form with descriptor and url inputs
- [x] 7.3 Add delete button (small icon) on each link row
- [x] 7.4 Wire add/delete actions to the store functions from 6.2
