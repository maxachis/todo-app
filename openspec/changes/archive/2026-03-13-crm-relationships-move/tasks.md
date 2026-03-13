## 1. Replace CRM Relationships Page

- [x] 1.1 Replace `frontend/src/routes/crm/relationships/+page.svelte` with the tabbed version from `frontend/src/routes/network/relationships/+page.svelte` (includes Person↔Person, Org→Person, and Org↔Org sub-tabs with full CRUD, filtering, inline editing, and type management)

## 2. Remove Network Relationships Route

- [x] 2.1 Delete `frontend/src/routes/network/relationships/+page.svelte`

## 3. Verify

- [x] 3.1 Run `cd frontend && npm run check` to confirm no TypeScript or Svelte errors
- [x] 3.2 Manually verify `/crm/relationships` loads with all three sub-tabs and CRUD works
- [x] 3.3 Verify `/network/relationships` returns 404
