## Context

The Relationships page has two panels (Person ↔ Person, Organization → Person), each with a create form and a flat list of all relationships. There's no way to filter the list or see an entity's existing connections at a glance. All data is already loaded client-side on mount (`personRelationships`, `orgRelationships`, `people`, `organizations`).

## Goals / Non-Goals

**Goals:**
- Let users filter the relationship list by a specific person or organization
- Auto-sync the filter when the form's primary field (Person A / Organization) is selected
- Exclude already-connected entities from the secondary dropdown (Person B / Person) to prevent duplicates and guide toward new connections

**Non-Goals:**
- No backend changes — all filtering is client-side over already-loaded arrays
- No changes to the TypeaheadSelect component — existing `options` prop filtering is sufficient
- No changes to the relationship data model

## Decisions

### 1. Filter control placement and type

**Decision**: Place a TypeaheadSelect between the create form and the relationship list in each panel, bound to a `filterPersonId` / `filterOrgId` state variable. Include a clear button (×) next to it.

**Rationale**: TypeaheadSelect is already used in the form fields and provides consistent UX. Placing it between form and list keeps the visual flow: create → filter → browse.

**Alternative considered**: A simple text search input. Rejected because it doesn't map cleanly to "filter by entity" semantics and would require fuzzy matching on displayed names.

### 2. One-way auto-sync from form to filter

**Decision**: When `newPerson1Id` changes (person panel) or `newOrgId` changes (org panel), auto-set the corresponding filter variable. When the form field is cleared, clear the filter. The filter is also independently editable — changing the filter does NOT update the form.

**Rationale**: The form drives context ("I'm about to create a relationship for this person, show me their connections"), but the filter should also work standalone for browsing. One-way sync avoids circular dependency.

### 3. Client-side filtering with $derived

**Decision**: Use Svelte 5 `$derived` to compute filtered lists:

```
Person panel:
  filteredPersonRelationships = filterPersonId
    ? personRelationships.filter(r => r.person_1_id === filterPersonId || r.person_2_id === filterPersonId)
    : personRelationships

Org panel:
  filteredOrgRelationships = filterOrgId
    ? orgRelationships.filter(r => r.organization_id === filterOrgId)
    : orgRelationships
```

**Rationale**: Data is already loaded in memory. Derived state is reactive and updates automatically. No API calls needed.

### 4. Excluding existing connections from secondary dropdown

**Decision**: Compute `availablePersonBOptions` and `availableOrgPersonOptions` as derived values that filter out IDs already connected to the selected primary entity.

```
Person panel (when Person A = John):
  connectedPersonIds = personRelationships
    .filter(r => r.person_1_id === john.id || r.person_2_id === john.id)
    .map(r => r.person_1_id === john.id ? r.person_2_id : r.person_1_id)

  Person B options = people.filter(p => p.id !== john.id && !connectedPersonIds.includes(p.id))

Org panel (when Org = Acme):
  connectedOrgPersonIds = orgRelationships
    .filter(r => r.organization_id === acme.id)
    .map(r => r.person_id)

  Person options = people.filter(p => !connectedOrgPersonIds.includes(p.id))
```

**Rationale**: Prevents duplicate relationship creation and naturally guides the user toward new connections. Uses the same `$derived` pattern for consistency.

### 5. Filter clear button

**Decision**: Add a small × button next to the filter TypeaheadSelect that clears the filter and shows all relationships again.

**Rationale**: Standard UX pattern for clearable filters. The TypeaheadSelect doesn't have built-in clear, so a sibling button handles it.

## Risks / Trade-offs

- **[Performance with large datasets]** → Client-side filtering is O(n) on every render. For a personal CRM with hundreds of relationships this is negligible. If it ever grew to thousands, the derived computations could be memoized, but this is unlikely for a single-user app.
- **[Filter state lost on navigation]** → Filter resets when leaving and returning to the Relationships page. This is acceptable since the filter is transient context, not persistent preference.
- **[Person B dropdown may be empty]** → If Person A already has relationships with everyone, the Person B dropdown shows no options. This is correct behavior — it means there's no one left to connect.
