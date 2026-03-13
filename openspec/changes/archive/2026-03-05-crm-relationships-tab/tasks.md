## 1. Move Relationships Route

- [x] 1.1 Move `frontend/src/routes/network/relationships/+page.svelte` to `frontend/src/routes/crm/relationships/+page.svelte`
- [x] 1.2 Delete the now-empty `frontend/src/routes/network/relationships/` directory

## 2. Update CRM Layout

- [x] 2.1 Add `{ href: '/crm/relationships', label: 'Relationships' }` tab to the CRM layout sub-tabs array in `frontend/src/routes/crm/+layout.svelte`

## 3. Simplify Network Layout

- [x] 3.1 Remove the "Relationships" tab from the Network layout sub-tabs in `frontend/src/routes/network/+layout.svelte`
- [x] 3.2 Remove the sub-tab navigation bar from the Network layout since only Graph remains
- [x] 3.3 Update `frontend/src/routes/network/+page.svelte` to redirect to `/network/graph` instead of `/network/relationships`

## 4. Verify

- [x] 4.1 Run `cd frontend && npm run check` to verify no TypeScript or Svelte errors
