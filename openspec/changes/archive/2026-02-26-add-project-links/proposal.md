## Why

Projects currently only have a name and description, with no way to associate external resources (GitHub repos, design docs, Figma files, deployed URLs, etc.). Adding project links lets users keep relevant URLs organized alongside their project without cluttering the description field.

## What Changes

- New `ProjectLink` model with a one-to-many relationship from `Project` (each project can have many links, each link belongs to one project)
- Each link stores a URL and a short descriptor/label (e.g., "GitHub Repo", "Figma Mockups", "Production URL")
- API endpoints for CRUD operations on project links, nested under the project resource
- Frontend UI on the Projects page to view, add, edit, and remove links from a project card
- Links render as clickable anchors opening in a new tab

## Non-goals

- Link validation beyond basic non-empty URL — no fetching link previews or checking reachability
- Ordering/sorting of links within a project
- Tagging or categorizing links beyond the free-text descriptor
- Sharing or exporting links independently from projects

## Capabilities

### New Capabilities

- `project-links`: CRUD management of URL links with descriptors attached to projects (model, API, and frontend UI)

### Modified Capabilities

_(none — the existing project model and UI are extended but no existing spec-level requirements change)_

## Impact

- **Backend**: New `ProjectLink` model in `tasks/models.py`, new migration, new API router in `tasks/api/` with nested endpoints under `/projects/{id}/links/`
- **Frontend**: Updated project card UI in `frontend/src/routes/projects/+page.svelte`, updated TypeScript types and API client, updated project store to handle link data
- **Database**: New `tasks_projectlink` table with FK to `tasks_project`
