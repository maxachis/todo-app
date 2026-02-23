## Context

The `TaskCreateForm` component currently has a title text input, an `<input type="date">` picker, and a "+" submit button. The date picker was added by the `add-task-inline-date` change and is bound to a `dueDate` state variable. The form sends `{ title, parent_id?, due_date? }` to the create API on submit.

The goal is to parse natural language date expressions from the title text as the user types, pre-fill the date picker with the detected date, and show a dismissible badge indicating detection occurred. The date picker remains the single source of truth for the due date.

## Goals / Non-Goals

**Goals:**
- Detect dates in common formats (natural language, numeric, month names) as the user types
- Pre-fill the existing date picker with the detected date
- Show a visual badge indicating a date was auto-detected, with a dismiss button
- Maintain the fast "type and Enter" workflow — detection must not interfere with typing
- Implement a clear state machine (LISTENING → SHOWING → DISMISSED) for detection lifecycle

**Non-Goals:**
- Modifying the title text (stripping date phrases) — the title is stored as-is
- Detecting or setting due times — only dates
- Replacing the manual date picker — it coexists with detection
- Debouncing — the input strings are short enough that per-keystroke parsing is fine
- Server-side date parsing — this is purely a frontend convenience feature

## Decisions

### 1. Use chrono-node for date parsing
**Choice**: Use `chrono-node` (npm package) to parse date expressions from the title text.
**Rationale**: Battle-tested library handling natural language ("tomorrow", "next friday"), numeric ("1/15", "01-15-2026"), and month name ("jan 15", "February 3rd") formats out of the box. Returns structured results including the matched text and parsed date. ~40KB gzipped — acceptable for the value it provides.
**Alternative considered**: Custom regex — rejected due to maintenance burden and poor natural language coverage.

### 2. Detection runs on every input event (no debounce)
**Choice**: Run `chrono.parseDate()` on each `input` event against the title text.
**Rationale**: Task titles are short (rarely > 100 chars). Chrono parsing a short string takes < 0.1ms — well within the 16ms frame budget. Debouncing would add complexity and introduce visible lag in badge appearance.

### 3. Three-state detection lifecycle
**Choice**: Manage detection state as a state machine with three states:
- **LISTENING**: Default state. Chrono runs on each input event. No badge shown.
- **SHOWING**: Chrono found a date. Badge is visible. Picker is pre-filled. If the user edits the text and chrono finds a new date, the badge and picker update. If chrono finds no date, the badge and picker value stick (date persists until explicitly dismissed).
- **DISMISSED**: User clicked ✕ on the badge. Detection stops. Picker is cleared. No further parsing until form resets.

Form submission or clearing the title resets to LISTENING.

**Rationale**: The "stick" behavior in SHOWING state prevents jarring disappearance while the user is mid-edit. The DISMISSED state gives users an explicit opt-out without the badge reappearing. Full reset on submit ensures each new task starts fresh.

### 4. Badge pre-fills the date picker (Scenario A)
**Choice**: When chrono detects a date, programmatically set the `dueDate` state variable (which is bound to the date picker). The date picker is the single source of truth.
**Rationale**: Avoids dual date state. The badge is purely a visual indicator that detection occurred — the actual date value lives in the picker. If the user manually changes the picker, the badge hides (explicit control takes priority). If the user dismisses the badge, the picker clears.

### 5. Badge positioned between title input and date picker
**Choice**: The detection badge appears as a small chip showing the formatted date and an ✕ button, positioned between the title input and the date picker in the form grid.
**Rationale**: The badge needs to be visually associated with the title (where the date was detected) while being close to the picker (which it pre-filled). On mobile, the pre-filled picker itself serves as the indicator — no separate badge element is needed to save space.

**Layout:**
```
Desktop:  [title___________] [Feb 24 ✕] [mm/dd/yy] [+]
Mobile:   [title___________] [02/24/2026] [+]  (badge hidden, picker shows value)
```

### 6. Manual picker selection hides the badge
**Choice**: When the user manually interacts with the date picker (changes its value directly), hide the badge and stop showing it for this input session. Detection continues running in the background (stays in LISTENING), but the badge won't reappear since the user has taken explicit control.
**Rationale**: If the user manually picks a date, they've overridden the suggestion. Showing the badge alongside a manually-set date would be confusing.

### 7. All state is local to the component
**Choice**: All detection state (current detection phase, detected date text, whether manually overridden) lives as local `$state` variables in `TaskCreateForm.svelte`. No stores needed.
**Rationale**: Detection is scoped to a single form instance. There's no reason for other components to know about detection state.

## Risks / Trade-offs

- **False positive detection** (e.g., "Call 311" → March 11, "Buy 2/4 lumber" → Feb 4) → Mitigation: The suggest-not-auto-set pattern means wrong detections are visible as a badge the user can dismiss. Chrono's heuristics handle most common false positives well. The title text is never modified.
- **Bundle size increase** (~40KB gzipped for chrono-node) → Acceptable for a single-user app. Could be lazy-loaded via dynamic import if needed later, but not worth the complexity now.
- **Badge adds visual noise to the form** → Mitigation: Badge is small, muted styling, only appears when a date is actually detected. Hidden on mobile (picker pre-fill serves as indicator).
- **Chrono locale assumptions** → Chrono defaults to English and US date conventions (month/day vs day/month). Acceptable for a single-user app. Could be configured later if needed.
