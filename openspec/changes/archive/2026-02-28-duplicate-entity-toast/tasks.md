## 1. Backend — Duplicate Detection

- [x] 1.1 Add duplicate check to `create_person` in `network/api/people.py`: before `Person.objects.create()`, query `Person.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).exists()` and raise `HttpError(409, {"detail": f"A person named {first_name} {last_name} already exists."})` if true
- [x] 1.2 Add duplicate check to `create_organization` in `network/api/organizations.py`: before `Organization.objects.create()`, query `Organization.objects.filter(name__iexact=name).exists()` and raise `HttpError(409, {"detail": f"An organization named {name} already exists."})` if true

## 2. Backend — Tests

- [x] 2.1 Add test in `network/` tests: POST `/api/people/` with a duplicate name returns 409 with expected detail message
- [x] 2.2 Add test in `network/` tests: POST `/api/people/` with a unique name still returns 201
- [x] 2.3 Add test in `network/` tests: POST `/api/organizations/` with a duplicate name returns 409 with expected detail message
- [x] 2.4 Add test in `network/` tests: POST `/api/organizations/` with a unique name still returns 201

## 3. Frontend — Toast on Duplicate

- [x] 3.1 In `frontend/src/routes/people/+page.svelte`, wrap the `api.people.create()` call in a try/catch; on a 409 response, call `addToast({ message: detail, type: 'error' })` and return early (do not clear the form)
- [x] 3.2 In `frontend/src/routes/organizations/+page.svelte`, wrap the `api.organizations.create()` call in a try/catch; on a 409 response, call `addToast({ message: detail, type: 'error' })` and return early (do not clear the form)
- [x] 3.3 Verify the `apiRequest` helper in `frontend/src/lib/api/client.ts` exposes HTTP status on errors so the frontend can distinguish 409 from other failures
