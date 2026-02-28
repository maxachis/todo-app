## 1. Backend Model & Migration

- [x] 1.1 Create `network/models/person_tag.py` with `PersonTag` model (name CharField, max 100, unique)
- [x] 1.2 Add `tags` ManyToManyField to `Person` model pointing to `PersonTag` (blank=True, related_name="people")
- [x] 1.3 Register `PersonTag` in `network/models/__init__.py`
- [x] 1.4 Generate and apply migration (`python manage.py makemigrations && python manage.py migrate`)

## 2. Backend API

- [x] 2.1 Add `PersonTagSchema` and `PersonTagInput` to `network/api/schemas.py`
- [x] 2.2 Update `PersonSchema` to include `tags: list[PersonTagSchema]`
- [x] 2.3 Update `_serialize_person` in `network/api/people.py` to include tags with prefetch
- [x] 2.4 Create `network/api/person_tags.py` router with: GET `/person-tags/` (list, with `exclude_person` param), POST `/people/{id}/tags/` (add, get_or_create), DELETE `/people/{id}/tags/{tag_id}/` (remove, 204)
- [x] 2.5 Add `tag` query parameter filter to GET `/people/` endpoint in `network/api/people.py`
- [x] 2.6 Register person_tags router in `network/api/__init__.py`

## 3. Frontend Types & API Client

- [x] 3.1 Add `PersonTag` interface to `frontend/src/lib/api/types.ts`
- [x] 3.2 Update `Person` interface to include `tags: PersonTag[]`
- [x] 3.3 Add API client methods in `frontend/src/lib/api/index.ts`: `personTags.list(excludePerson?)`, `people.addTag(personId, name)`, `people.removeTag(personId, tagId)`

## 4. Frontend Person Detail

- [x] 4.1 Add tag display section to person detail view in `frontend/src/routes/people/+page.svelte` — after contact fields, before notes — showing tags with remove buttons
- [x] 4.2 Add TypeaheadSelect for tags with `onCreate` callback for inline tag creation
- [x] 4.3 Wire up add/remove tag API calls with optimistic UI updates

## 5. Frontend People List

- [x] 5.1 Display tags inline on each person row in the people list
- [x] 5.2 Add tag filter control (dropdown or TypeaheadSelect) to the people list, placed near the sort controls
- [x] 5.3 Wire tag filter to re-fetch people list with `?tag=` query parameter

## 6. Verification

- [x] 6.1 Test backend: create person tags, add/remove from people, filter people by tag, verify API responses include tags
- [x] 6.2 Test frontend: `npm run check` passes with no type errors
- [ ] 6.3 Manual test: full flow — create tags, assign to people, filter list, remove tags
