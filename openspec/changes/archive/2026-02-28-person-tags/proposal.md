## Why

People in the network/CRM have no way to be organized beyond name and last-interaction metadata. Users need a lightweight, user-driven tagging system to categorize individuals (e.g., "investor", "mentor", "client", "college") so they can quickly filter and find relevant contacts.

## What Changes

- New `PersonTag` model with a simple `name` field, separate from the existing task `Tag` model — different domains, different vocabularies.
- M2M relationship between `Person` and `PersonTag`.
- API endpoints to list person tags, add/remove tags on a person, and filter the people list by tag.
- Person detail view gains a TypeaheadSelect for tags near the top (above notes).
- People list shows tags inline on each row and supports filtering by tag.

## Non-goals

- Sharing tags between tasks and people (explicitly decided against — different vocabularies).
- Tagging organizations (covered by `OrgType`).
- Tag colors, hierarchies, or metadata beyond the name.

## Capabilities

### New Capabilities
- `person-tags`: Tagging system for people — model, API, detail view editing, list display, and list filtering.

### Modified Capabilities
- `network-domain-model`: Person model gains a M2M relationship to PersonTag.
- `network-api`: New endpoints for person tag management and people list filtering by tag.
- `network-frontend`: Person detail and people list UI updated to support tags.

## Impact

- **Backend**: New model + migration in `network/models/`, new API router in `network/api/`, schema updates.
- **Frontend**: Type updates, new API client methods, person detail component changes, people list component changes.
- **Database**: New `PersonTag` table and M2M join table.
