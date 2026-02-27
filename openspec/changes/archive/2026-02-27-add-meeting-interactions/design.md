## Context

The Interaction model currently has a single `person` ForeignKey — each interaction record is associated with exactly one person. This makes it impossible to represent a meeting with multiple attendees as a single event. Users must create duplicate interaction records (same date, type, notes) for each person involved, losing the shared context.

The change replaces this FK with a many-to-many relationship so a single interaction can reference multiple people.

## Goals / Non-Goals

**Goals:**
- Allow an interaction to be associated with one or more people
- Preserve existing single-person workflow (creating an interaction with one person should feel the same)
- Migrate all existing data without loss
- Update the People API `last_interaction_date`/`last_interaction_type` annotations to work with the new M2M relationship

**Non-Goals:**
- Separate "Meeting" entity or model — an interaction with multiple people is sufficient
- Calendar/scheduling integration
- Required minimum attendees — an interaction with zero people is allowed (though unusual)
- Changing interaction types or adding "Meeting" as a special type

## Decisions

### 1. M2M through table vs. explicit through model

**Decision:** Use Django's default auto-generated M2M table (`Interaction.people = ManyToManyField(Person, blank=True)`).

**Alternatives considered:**
- Explicit through model with extra fields (e.g., role, attendance status) — rejected because there's no current need for per-attendee metadata. Can be added later by converting to an explicit through model if needed.

**Rationale:** Keeps things simple. The auto-generated `network_interaction_people` table is sufficient. Django supports migrating from implicit to explicit through models later.

### 2. Migration strategy

**Decision:** Two-step migration:
1. Schema migration: Add the new `people` M2M field (keeping the old `person` FK temporarily)
2. Data migration: For each existing interaction, add `interaction.people.add(interaction.person_id)`
3. Schema migration: Remove the old `person` FK, making `people` the sole relationship

**Rationale:** This ensures zero data loss and is straightforward to test. The old FK is kept through the data migration step so we can reference it.

### 3. API schema change

**Decision:** Replace `person_id: int` with `person_ids: list[int]` in create/update/response schemas.

- **Create**: `person_ids` is required, must contain at least one ID
- **Update**: `person_ids` is optional (omit to leave unchanged); when provided, replaces the full set
- **Response**: Always includes `person_ids: list[int]`

**Alternatives considered:**
- Keeping `person_id` alongside `person_ids` for backward compatibility — rejected because this is a single-user app with no external API consumers. Clean break is simpler.
- Add/remove endpoints for individual people — over-engineering for this use case. The set-replace approach on update is sufficient.

### 4. Frontend multi-person selection

**Decision:** Reuse the existing `TypeaheadSelect` component but allow multiple selections. The component currently supports single-select (`value` binding returns one ID). The approach:

- Create a new wrapper component or extend the interaction form to use TypeaheadSelect in `onSelect` callback mode (already supported) to add people one at a time
- Display selected people as removable chips/tags above or below the input
- The TypeaheadSelect already supports `onSelect` callback mode which doesn't bind a single value — perfect for "add to list" behavior

**Alternatives considered:**
- Build a dedicated MultiTypeaheadSelect component — more work, and the existing onSelect mode already handles this pattern
- Checkboxes for all people — doesn't scale, no search/filter

### 5. People API annotation update

**Decision:** Update `_annotate_people` in `network/api/people.py` to use the M2M reverse relationship. The `Max("interaction__date")` annotation path changes because the reverse accessor changes from `interaction_set` (FK) to the M2M reverse. With Django M2M, the annotation `Max("interaction__date")` still works because Django resolves the reverse M2M lookup the same way. The Subquery for `last_interaction_type` needs to filter via the M2M through table instead of `person=OuterRef("pk")`.

## Risks / Trade-offs

- **Breaking API change** → Acceptable for single-user app. Frontend and backend are deployed together, so no version mismatch risk.
- **Data migration on existing interactions** → Low risk. Migration is additive (copies FK value to M2M set), then removes FK. Easily reversible by restoring from backup if needed.
- **M2M queries slightly more complex** → Interaction list queries now need a prefetch for people. Minor performance impact on SQLite with small dataset.
- **Interaction list display** → Showing multiple names per interaction row needs care to avoid layout overflow. Will truncate after 2-3 names with "+N more" indicator.

## Migration Plan

1. Add `people` M2M field to Interaction model (schema migration)
2. Run data migration to copy each `interaction.person_id` into `interaction.people`
3. Remove `person` FK from Interaction model (schema migration)
4. Update API schemas and router
5. Update frontend types and interaction page
6. Update people API annotations

**Rollback:** Revert migrations. Since SQLite is file-based, a pre-migration backup of `db.sqlite3` provides a simple rollback path.

## Open Questions

None — the scope is well-defined and the implementation is straightforward.
