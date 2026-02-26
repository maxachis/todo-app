## 1. Backend Models & Migration

- [x] 1.1 Create `network/models/lead.py` with Lead model (title, status with choices, notes, person FK SET_NULL, organization FK SET_NULL, created_at, updated_at) and CheckConstraint requiring at least one of person/organization
- [x] 1.2 Create `network/models/lead_task.py` with LeadTask link model (lead FK CASCADE, task FK CASCADE, created_at, unique constraint on lead+task pair)
- [x] 1.3 Register both models in `network/models/__init__.py`
- [x] 1.4 Run `makemigrations` and `migrate` to create the migration

## 2. Backend API

- [x] 2.1 Add Lead and LeadTask schemas to `network/api/schemas.py` (LeadSchema, LeadCreateInput, LeadUpdateInput, LeadTaskSchema)
- [x] 2.2 Create `network/api/leads.py` router with CRUD endpoints: GET /leads/ (list, ordered by -updated_at, annotated with person_name and organization_name), POST /leads/ (201), GET /leads/{id}/, PUT /leads/{id}/, DELETE /leads/{id}/ (204)
- [x] 2.3 Add lead-task link endpoints to leads router: GET /leads/{lead_id}/tasks/, POST /leads/{lead_id}/tasks/ (get_or_create, 201/200), DELETE /leads/{lead_id}/tasks/{task_id}/ (204)
- [x] 2.4 Register leads router in `network/api/__init__.py`

## 3. Backend Tests

- [x] 3.1 Create `network/tests/test_api_leads.py` with tests for Lead CRUD (create, list, get, update, delete) and validation (reject lead with no person or org)
- [x] 3.2 Add tests for lead-task link endpoints (link, list, unlink, duplicate handling)

## 4. Frontend API Client

- [x] 4.1 Add Lead, CreateLeadInput, UpdateLeadInput interfaces to `frontend/src/lib/api/types.ts`
- [x] 4.2 Add `leads` namespace to `frontend/src/lib/api/index.ts` with getAll, get, create, update, remove methods
- [x] 4.3 Add `leads` to `taskLinks` namespace in `frontend/src/lib/api/index.ts` with listByLead, add, remove methods

## 5. Frontend Page

- [x] 5.1 Create `frontend/src/routes/leads/+page.svelte` with two-panel layout: left list panel (creation form, scrollable lead list with title/contact/status badge) and right detail panel (editable title, status selector, person/org typeaheads, notes, linked tasks)
- [x] 5.2 Add "Leads" tab to nav in `frontend/src/routes/+layout.svelte` after Graph, before Projects

## 6. Verification

- [x] 6.1 Run backend tests (`uv run python -m pytest network/tests/test_api_leads.py -q`)
- [x] 6.2 Run frontend type check (`cd frontend && npm run check`)
- [ ] 6.3 Manual smoke test: create lead, edit fields, link tasks, verify list updates
