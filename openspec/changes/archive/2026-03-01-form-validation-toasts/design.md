## Context

All forms in the app currently validate required fields with inline checks (`if (!field.trim()) return;`) and silently abort on failure. The toast system (`addToast`) is mature and already used for API errors, but never for validation feedback. There are ~12 submit handlers across 8 route files and 2 components, each with hand-written validation logic.

## Goals / Non-Goals

**Goals:**

- Give users immediate feedback when a form submission fails due to missing required fields.
- Consolidate repeated validation patterns into a single reusable helper to reduce duplication and ensure consistent messaging.

**Non-Goals:**

- Field-level inline error UI (red borders, error text beneath inputs).
- Changing the toast component or store API.
- Touching backend validation or API error handling.
- Adding success toasts on form submit (keep existing behavior of just refreshing the list).

## Decisions

### 1. Shared `validateRequired` helper in `$lib/utils/validation.ts`

**Choice:** A single function that takes a record of `{ fieldLabel: value }` pairs, checks each for empty/null/undefined, and calls `addToast` with a message listing the missing fields. Returns `true` if valid, `false` if not.

**Rationale:** Every form does the same thing — check `.trim()` or `!= null` — but with bespoke inline code. A declarative helper eliminates duplication while keeping each form's submit handler in control (no framework-level form abstraction needed).

**Alternatives considered:**
- *Per-form inline toasts (no helper)*: Simplest change, but duplicates message formatting logic 12+ times and risks inconsistent wording.
- *Svelte action or form component wrapper*: Over-engineered for a single-user app; adds indirection without proportional benefit.

**API:**

```ts
// $lib/utils/validation.ts
import { addToast } from '$lib/stores/toast';

type FieldValue = string | number | null | undefined | unknown[];

export function validateRequired(fields: Record<string, FieldValue>): boolean {
  const missing = Object.entries(fields)
    .filter(([, v]) => {
      if (v == null) return true;
      if (typeof v === 'string') return v.trim() === '';
      if (Array.isArray(v)) return v.length === 0;
      return false;
    })
    .map(([label]) => label);

  if (missing.length > 0) {
    addToast({
      message: `Required: ${missing.join(', ')}`,
      type: 'error'
    });
    return false;
  }
  return true;
}
```

### 2. Replace inline checks with `validateRequired` calls

**Choice:** Each form's submit handler replaces its `if (!x.trim() || !y) return;` with:

```ts
if (!validateRequired({ 'First name': newFirst, 'Last name': newLast })) return;
```

**Rationale:** Minimal diff per form — one import and one line change. The handler still early-returns, preserving existing control flow. Labels are human-readable strings used directly in the toast message.

### 3. Toast type and auto-dismiss

**Choice:** Use `type: 'error'` with the default 5-second auto-dismiss.

**Rationale:** Error type gives the red styling that communicates "something went wrong." 5 seconds is enough to read a short message, and the user can retry immediately. No need for a sticky/persistent toast since the form state is unchanged (they can just fill in the field and resubmit).

## Risks / Trade-offs

- **Toast fatigue**: If a user repeatedly submits an empty form, they'll get repeated toasts. Mitigation: the 5s auto-dismiss keeps the stack from growing unboundedly, and this is a single-user app so the pattern is self-correcting.
- **Label accuracy**: Field labels in `validateRequired` calls are hardcoded strings — if the UI label changes, the toast message could drift. Mitigation: labels are co-located with the form markup, so they'll be updated together in practice.
- **Edit/save forms**: Some detail panels auto-save on blur (people, orgs, leads). These don't have a submit event to intercept. Decision: leave blur-save forms unchanged — they already work because the field can't be blanked (it reverts to the last saved value). Only create-form submit handlers get the new validation.
