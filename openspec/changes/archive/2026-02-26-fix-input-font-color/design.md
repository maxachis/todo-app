## Context

The app uses CSS custom properties for theming, defined in `+layout.svelte`. Two variables control input styling: `--bg-input` (background) and `--text-primary` (text color). Several inline-edit input fields were implemented without setting `background`, causing them to inherit browser defaults. In dark mode, this results in bright (white) input backgrounds with bright text — nearly unreadable.

Components already correctly styled (TaskDetail, TaskCreateForm, RecurrenceEditor, TypeaheadSelect) use `background: var(--bg-input)` and `color: var(--text-primary)`. The fix applies the same pattern to the remaining inputs.

## Goals / Non-Goals

**Goals:**
- All inline-edit inputs use `background: var(--bg-input)` and `color: var(--text-primary)`
- Consistent input appearance across light, dark, and system theme modes

**Non-Goals:**
- Introducing a global input reset or base input class
- Changing the CSS variable values themselves
- Modifying focus/active states or border styling

## Decisions

**Decision: Add properties directly to each component's scoped CSS**

Add `background: var(--bg-input)` (and `color: var(--text-primary)` where missing) to each affected component's existing `<style>` block rather than introducing a global input style rule.

*Rationale*: The app uses Svelte scoped styles throughout. A global rule would break the existing pattern and risk unintended side effects on inputs that have intentionally different styling (e.g., search bar, date picker). The fix is small (5 components, one property each) and matches how correctly-styled components already work.

*Alternative considered*: A global `input, textarea { background: var(--bg-input); color: var(--text-primary); }` rule in `+layout.svelte`. Rejected because it would affect all inputs indiscriminately and could interfere with components that set their own background intentionally.

## Risks / Trade-offs

- **[Low] Visual regression in light mode** → In light mode, `--bg-input` is `#ffffff`, which matches the browser default for inputs, so no visible change. Verify by visual inspection.
- **[Low] Missed inputs** → The audit identified 5 affected components. If others exist, they can be fixed the same way in a follow-up.
