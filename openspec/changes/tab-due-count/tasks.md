## 1. Derived count store

- [x] 1.1 Create a derived store in `frontend/src/lib/stores/upcoming.ts` that computes the count of overdue + due-today tasks from `upcomingStore`

## 2. Document title reactivity

- [x] 2.1 In `frontend/src/routes/+layout.svelte`, import the count store and add an `$effect` that sets `document.title` to `(N) Nexus` or `Nexus` based on the count

## 3. Load upcoming data on app init

- [x] 3.1 In `frontend/src/routes/+layout.svelte`, call `loadUpcoming()` on mount so the count is available regardless of initial route

## 4. Verification

- [x] 4.1 Run `npm run check` to verify no type errors
- [x] 4.2 Manual verification: confirm tab title shows count on Tasks page and updates when completing a task
