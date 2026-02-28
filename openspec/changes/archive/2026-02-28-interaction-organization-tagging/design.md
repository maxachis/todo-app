## Context

Interactions currently link to people via a Django ManyToManyField (`people`) directly on the `Interaction` model. The API serializes this as `person_ids: list[int]` and the frontend renders a TypeaheadSelect multi-chip picker for people in both the create and edit forms.

Organizations exist as a separate model but have no relationship to interactions. This change adds that relationship.

## Goals / Non-Goals

**Goals:**
- Allow tagging zero or more organizations on any interaction
- Follow the exact same pattern as the existing `people` M2M field for consistency
- Expose `organization_ids` in the API alongside `person_ids`
- Provide organization multi-select in the create and edit UI using TypeaheadSelect

**Non-Goals:**
- Organization filtering/search on interactions
- Required organization field (organizations remain fully optional)
- Inline organization creation from the interaction form

## Decisions

### 1. M2M field on Interaction model (not explicit link table)

**Choice**: Add `organizations = ManyToManyField("network.Organization", related_name="interactions", blank=True)` directly on the `Interaction` model.

**Rationale**: This mirrors how `people` is implemented on the same model. Using an explicit link model (like `InteractionTask` in `task_links.py`) would be inconsistent and add unnecessary complexity for a simple many-to-many association with no extra fields.

**Alternative considered**: Explicit `InteractionOrganization` model in `task_links.py` — rejected because it doesn't match the people pattern and adds code for no benefit.

### 2. API changes inline with existing endpoint

**Choice**: Extend the existing `/api/interactions/` create/update/response schemas to include `organization_ids` as an optional list of integers.

**Rationale**: Keeps the API surface simple — one endpoint handles the full interaction, rather than requiring separate link/unlink calls. This matches how `person_ids` works today.

### 3. Frontend: TypeaheadSelect chip pattern

**Choice**: Reuse the same TypeaheadSelect multi-chip pattern used for people selection, placed below the people selector in both create and edit forms.

**Rationale**: Consistent UX. Users already understand the chip selection pattern from picking people.

### 4. Organizations optional, no minimum requirement

**Choice**: Unlike `person_ids` which requires at least one person, `organization_ids` defaults to an empty list and has no minimum.

**Rationale**: Many interactions don't involve an organization. This keeps the workflow frictionless.

## Risks / Trade-offs

- **Migration**: Simple schema migration adding an M2M table — no data migration needed since no existing interactions have organizations. Risk is minimal.
- **UI density**: Adding another selector to the interaction form increases visual complexity. Mitigated by placing it after the people selector where it's logically grouped.
