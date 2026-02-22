## Context

The People page is a list+detail CRUD view (`frontend/src/routes/people/+page.svelte`). The backend API (`network/api/people.py`) returns person records with no interaction data. Interactions are stored in a separate `Interaction` model linked to `Person` via `person` FK. Follow-up cadence is stored on `Person.follow_up_cadence_days`. There are currently 54 people, 41 with cadences set, and 63 interactions — most from late January, meaning nearly everyone is overdue as of late February.

## Goals / Non-Goals

**Goals:**
- Surface follow-up urgency directly in the People list without requiring cross-referencing the Interactions page
- Let users sort by follow-up urgency to triage who needs attention first
- Show last interaction context in the detail panel so the user knows what they last did
- Allow quick interaction logging from the People page to close the triage-act loop

**Non-Goals:**
- A separate dashboard or follow-up page — the People page is the right home
- Charts or graphs — status indicators and sorted lists are sufficient
- Notifications or reminders — this is a pull-based view, not push
- Changing how interactions are stored or modeled

## Decisions

### 1. Compute follow-up status on the backend via annotation

Annotate the people queryset with `Max('interaction__date')` and a subquery for the latest interaction type name. Return `last_interaction_date` and `last_interaction_type` as computed fields on PersonSchema.

**Why over frontend computation:** The frontend would need to fetch all interactions for all people just to compute status. A single annotated query is simpler and keeps the API as the source of truth.

**Why over a denormalized field:** With 54 people and 63 interactions, the annotation query is trivial for SQLite. Denormalization would require keeping it in sync on every interaction create/update/delete — not worth the complexity.

### 2. Follow-up status tiers computed on the frontend

The API returns raw data (`last_interaction_date`, `follow_up_cadence_days`). The frontend computes the status tier:
- **Overdue**: days since last interaction > cadence
- **Due soon**: days since > cadence * 0.8 (within 20% of cadence)
- **On track**: days since <= cadence * 0.8
- **No cadence**: `follow_up_cadence_days` is null — no status shown
- **Never contacted**: has cadence but no interactions — treated as overdue

**Why frontend:** Status tiers are a display concern. The thresholds may evolve with user preference. Keeping them in the frontend avoids API changes for presentation tweaks.

### 3. Sort by "overdue ratio" for urgency ordering

Sort value = `days_since_last_interaction / follow_up_cadence_days`. Higher ratio = more overdue relative to their cadence. People with no cadence sort to the bottom. People never contacted with a cadence sort to the top (infinite ratio).

**Why ratio over absolute days:** Someone 30 days overdue on a 7-day cadence (4.3x) is more urgent than someone 30 days overdue on a 60-day cadence (0.5x — actually not even overdue). The ratio captures relative urgency.

### 4. Quick-log form in detail panel, not inline in list

Place the quick-log interaction form in the People detail panel below the last-interaction summary. It creates an Interaction record via the existing `POST /api/interactions/` endpoint, then refreshes the people list to update the status.

**Why detail panel:** The list items are already dense with status info. An inline form per row would be overwhelming. The detail panel has space, and clicking a person to act on them is the natural flow.

### 5. Reuse existing interaction creation API

The quick-log form calls the same `POST /api/interactions/` endpoint used by the Interactions page. No new backend endpoint needed. After creation, reload the people list to pick up the updated `last_interaction_date`.

## Risks / Trade-offs

**[Annotation query performance at scale]** → With SQLite and <100 people, this is a non-issue. If the dataset grows significantly, the subquery annotation could be replaced with a denormalized field. No action needed now.

**[Quick-log duplicates full interaction creation]** → The quick-log form is a simplified version of the Interactions page form. If interaction creation logic changes, both places need updating. Acceptable given the simplicity and the value of not leaving the page.

**[Status thresholds are hardcoded]** → The 0.8 multiplier for "due soon" is a reasonable default. If the user wants to customize thresholds later, it can be extracted to a constant or setting. No action needed now.
