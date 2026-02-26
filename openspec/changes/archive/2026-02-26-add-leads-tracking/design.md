## Context

The app's network domain tracks people, organizations, interactions, and relationships. Business development leads — potential work opportunities tied to contacts — are currently tracked outside the system. The existing network domain provides the entity model and link table patterns that leads will follow.

## Goals / Non-Goals

**Goals:**
- Add a Lead entity to the network domain with person/org associations
- Provide full CRUD API following existing Django Ninja router patterns
- Build a two-panel list+detail page consistent with People/Organizations pages
- Support linking tasks to leads via a dedicated link table

**Non-Goals:**
- Kanban/pipeline board UI
- Lead analytics, reporting, or revenue tracking
- Automated status transitions or lead-to-project conversion
- Drag-and-drop reordering of leads

## Decisions

### Lead model lives in the network app
**Rationale:** Leads are network entities — they reference people and organizations. Placing the model in `network/models/` keeps the network domain cohesive. The `LeadTask` link table follows the exact pattern of `TaskPerson`, `TaskOrganization`, and `InteractionTask` in `network/models/task_links.py`.

**Alternative considered:** Putting leads in the `tasks` app since they link to tasks. Rejected because the primary associations are with people/organizations, and the tasks app focuses on task hierarchy and scheduling.

### Status as a CharField with choices (not a separate model)
**Rationale:** The five statuses (prospect, interested, committed, fulfilled, unfulfilled) are a fixed, small set that maps to a sales pipeline. Unlike org types or interaction types (which users may want to extend), lead statuses represent a defined workflow. CharField with choices avoids an unnecessary join and extra migration for seed data.

**Alternative considered:** A LeadStatus lookup table (like OrgType/InteractionType). Rejected because the status set is stable and doesn't benefit from user extensibility.

### Check constraint: at least one of person or organization required
**Rationale:** A lead without any contact association is meaningless. The proposal specifies both FKs as optional (a lead can relate to just a person, just an org, or both), but at least one must be set. A database-level CheckConstraint enforces this invariantly, matching the pattern used for relationship normalization in `RelationshipPersonPerson`.

### Two-panel page layout (not three-panel)
**Rationale:** Leads don't have a hierarchical structure like tasks (lists → sections → tasks). The People and Organizations pages use a two-panel list+detail layout, which is the natural fit. The left panel shows the lead list with inline creation form; the right panel shows editable detail with linked tasks.

### Nav tab placement: after Graph, before Projects
**Rationale:** Leads are a network/CRM concept, so they belong in the network cluster of tabs (People, Orgs, Interactions, Relationships, Graph). Placing "Leads" after Graph keeps it in the network group while being visually distinct as the last network-related tab.

## Risks / Trade-offs

**Lead-person/org deletion cascade** → Use `SET_NULL` on person and organization FKs so leads survive contact deletion. The check constraint allows both to be null only if the other is set, but if both get deleted the lead becomes orphaned. Mitigation: this is acceptable for a single-user app; the user can manually clean up orphaned leads.

**No store-level reactivity for cross-entity updates** → If a person is deleted on the People page, the Leads page won't reflect it until reload. Mitigation: consistent with existing behavior across People/Orgs/Interactions pages — each page manages its own data lifecycle.
