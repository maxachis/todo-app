## Context

Interactions currently have a single classification axis — `InteractionType` (the "what": Meeting, Catch-up, Introduction). Users want a second axis — medium (the "how": Email, Phone, In-Person, Video) — to capture richer metadata. The medium is optional, since some interactions don't have a clear medium or the user may not care to specify.

The codebase already has an established pattern for simple name-only reference models (`InteractionType`, `OrgType`) with corresponding CRUD API routers, frontend API client methods, and TypeaheadSelect integration with inline creation.

## Goals / Non-Goals

**Goals:**
- Add `InteractionMedium` as a first-class model following existing patterns
- Expose full CRUD API for mediums
- Allow optional medium selection (with inline creation) on interaction create/edit forms
- Display medium in interaction list items when present

**Non-Goals:**
- Filtering or grouping interactions by medium (future work)
- Migrating existing data or splitting existing interaction types
- Making medium required

## Decisions

### 1. Full model vs. CharField choices

**Decision**: Full `InteractionMedium` model with FK on `Interaction`

**Rationale**: The user wants the same TypeaheadSelect + inline creation UX as interaction types. A `CharField(choices=...)` would require code changes to add new mediums, breaking the self-service pattern. The overhead of a small model + CRUD router is minimal and consistent with `InteractionType` and `OrgType`.

**Alternative considered**: `CharField(choices=MEDIUM_CHOICES)` — simpler but no inline creation, requires code deploy to add mediums.

### 2. FK constraint: RESTRICT vs. SET_NULL

**Decision**: `on_delete=models.SET_NULL` (with `null=True, blank=True`)

**Rationale**: If a medium is deleted, existing interactions should remain intact with medium cleared to null. This is different from `InteractionType` which uses `RESTRICT` (type is required). Since medium is optional, SET_NULL is the natural choice — it avoids blocking medium deletion while preserving interaction records.

### 3. API endpoint naming

**Decision**: `/api/interaction-mediums/` following the existing `/api/interaction-types/` convention.

### 4. Frontend state management

**Decision**: Load mediums alongside interaction types in the existing `loadData()` function on the interactions page. No dedicated Svelte store needed — the interactions page is the only consumer, matching how interaction types are currently handled (local component state, not a store).

## Risks / Trade-offs

- **Two dropdowns on the form** → Slightly more visual complexity. Mitigated by medium being optional and positioned after the type field.
- **Name collisions** → Users could create mediums with the same name as types (e.g., "Email" as both a type and medium). This is acceptable — they represent different dimensions and the labels are in separate fields.
