## 1. Backend: Add last-interaction fields to People API

- [x] 1.1 Add `last_interaction_date: Optional[date]` and `last_interaction_type: Optional[str]` to `PersonSchema` in `network/api/schemas.py`
- [x] 1.2 Update `_serialize_person()` in `network/api/people.py` to accept and pass through the new fields
- [x] 1.3 Annotate the `list_people` queryset with `Max('interaction__date')` and a subquery for the latest interaction type name
- [x] 1.4 Annotate the `get_person` queryset similarly so single-person detail includes the fields
- [x] 1.5 Ensure `create_person` and `update_person` return the new fields (null for new people with no interactions)

## 2. Frontend: Update Person type and API client

- [x] 2.1 Add `last_interaction_date: string | null` and `last_interaction_type: string | null` to the `Person` type in `frontend/src/lib/api/`

## 3. Frontend: Follow-up status indicators in People list

- [x] 3.1 Add a helper function to compute follow-up status tier (overdue / due-soon / on-track / no-cadence) and days-since from `last_interaction_date` and `follow_up_cadence_days`
- [x] 3.2 Display status indicator and "Xd / Yd" text on each list item in `frontend/src/routes/people/+page.svelte`, color-coded by tier
- [x] 3.3 Show "never / Yd" for people with cadence but null `last_interaction_date`
- [x] 3.4 Show no indicator for people with null cadence

## 4. Frontend: Follow-up status sort option

- [x] 4.1 Add `'follow_up_status'` to the `sortField` type and add it as an option in the sort dropdown in `frontend/src/routes/people/+page.svelte`
- [x] 4.2 Implement sort logic: compute overdue ratio (`days_since / cadence`), sort descending by default, null-cadence people to bottom, never-contacted people with cadence to top

## 5. Frontend: Last interaction summary in detail panel

- [x] 5.1 Display "Last interaction: {date} - {type}" in the detail panel when a person is selected and has `last_interaction_date`
- [x] 5.2 Display an overdue warning when the person's days since last interaction exceeds their cadence

## 6. Frontend: Quick-log interaction form in detail panel

- [x] 6.1 Load interaction types on the People page (reuse `api.interactionTypes.getAll()`)
- [x] 6.2 Add an inline form in the detail panel with interaction type selector (TypeaheadSelect) and date input defaulting to today
- [x] 6.3 On submit, call `api.interactions.create()` with the selected person, type, and date, then reload the people list to update status
- [x] 6.4 Clear the form after successful submission

## 7. Testing

- [x] 7.1 Add API test in `network/tests/` verifying `last_interaction_date` and `last_interaction_type` are returned correctly for people with and without interactions
- [x] 7.2 Verify the annotation returns the most recent interaction when multiple exist
