## Why

The app tracks people and organizations but has no way to represent business development leads — potential work opportunities tied to those contacts. Without this, lead tracking happens outside the system (mental notes, spreadsheets), disconnected from the people, orgs, tasks, and interactions already being managed here.

## What Changes

- New `Lead` model in the network domain with title, status (prospect/interested/committed/fulfilled/unfulfilled), notes, optional person FK, optional org FK, and a check constraint requiring at least one of person or organization
- New `LeadTask` link table associating leads with tasks
- New Django Ninja API endpoints for CRUD on leads and lead-task links
- New top-level "Leads" nav tab with a list+detail two-panel page (consistent with People/Organizations page pattern)
- Lead list shows title, associated person/org, and status badge
- Lead detail panel shows editable fields, status selector, notes, and linked tasks

## Capabilities

### New Capabilities
- `leads`: Lead entity model, statuses, person/org associations, lead-task links, API endpoints, and frontend page

### Modified Capabilities
- `network-domain-model`: Adding Lead and LeadTask as new network entities with FKs to Person, Organization, and Task

## Non-goals

- Kanban/pipeline board UI (list view only for now)
- Lead analytics or reporting
- Automated status transitions
- Lead-to-project conversion workflow
- Dollar values or expected revenue tracking

## Impact

- **Backend**: New model + migration in `network`, new API router in `network/api/`
- **Frontend**: New route at `/leads`, new nav tab in layout, new API client methods
- **Database**: New `network_lead` and `network_leadtask` tables
- **Existing code**: Minor change to nav layout to add the Leads tab; no changes to existing People/Org/Task behavior
