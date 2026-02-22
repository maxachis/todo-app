## 1. Model and Migration

- [x] 1.1 Add `email` (CharField, max_length=255, blank=True) and `linkedin_url` (CharField, max_length=500, blank=True) to `network/models/person.py`
- [x] 1.2 Generate and run migration: `python manage.py makemigrations && python manage.py migrate`

## 2. API Schemas

- [x] 2.1 Add `email` and `linkedin_url` to `PersonSchema` response in `network/api/schemas.py`
- [x] 2.2 Add `email: str = ""` and `linkedin_url: str = ""` to `PersonCreateInput` in `network/api/schemas.py`
- [x] 2.3 Add `email: Optional[str] = None` and `linkedin_url: Optional[str] = None` to `PersonUpdateInput` in `network/api/schemas.py`

## 3. Frontend Types

- [x] 3.1 Add `email: string` and `linkedin_url: string` to `Person` interface in `frontend/src/lib/api/types.ts`
- [x] 3.2 Add `email?: string` and `linkedin_url?: string` to `CreatePersonInput` and `UpdatePersonInput` in `frontend/src/lib/api/types.ts`

## 4. Frontend Create Form

- [x] 4.1 Add `newEmail` and `newLinkedin` state variables to `frontend/src/routes/people/+page.svelte`
- [x] 4.2 Add email (`type="email"`) and LinkedIn URL text inputs to the create form, after name fields and before follow-up cadence
- [x] 4.3 Pass `email` and `linkedin_url` in the `api.people.create()` call and reset state after creation

## 5. Frontend Edit Form and Detail View

- [x] 5.1 Add `editEmail` and `editLinkedin` state variables, populated when a person is selected
- [x] 5.2 Add email and LinkedIn URL inputs to the edit form in the detail panel
- [x] 5.3 Include `email` and `linkedin_url` in the `api.people.update()` call on save
- [x] 5.4 Display non-empty email as `mailto:` link and LinkedIn as external link (target="_blank") in the detail panel above the edit form

## 6. Verify

- [x] 6.1 Run `cd frontend && npm run check` to confirm no type errors
- [x] 6.2 Run `uv run python -m pytest tasks/tests/test_api_setup.py -q` to confirm backend tests pass
