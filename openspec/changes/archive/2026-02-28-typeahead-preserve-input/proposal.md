## Why

In bound-value mode, when the user types text into a TypeaheadSelect that doesn't match any existing option and then loses focus (clicks away, tabs out), the typed text is silently eliminated. This is disorienting — the user's input vanishes with no feedback. The problem is worst on fields without `onCreate` (e.g., organization/person selectors on Relationships and Leads pages) where "No match found — add it first" appears but the text still disappears on blur, but it also affects fields with `onCreate` when the user clicks away before selecting the "Create" option.

## What Changes

- In bound-value mode, when the user blurs the TypeaheadSelect with unmatched text and `onCreate` is available, auto-trigger creation instead of silently discarding the input
- In bound-value mode without `onCreate`, preserve the typed text on blur and show a visual indication that the value is invalid/unresolved rather than silently clearing it
- On Escape in bound-value mode with no prior selection, clear the input (explicit user intent to cancel)

## Capabilities

### New Capabilities

_None_

### Modified Capabilities

- `typeahead-selector`: Add blur behavior for unmatched text — auto-create when `onCreate` is available; preserve-with-warning when it is not

## Non-goals

- Changing action mode (onSelect) blur behavior — action mode already clears correctly
- Adding free-text input support — the component remains a selector, not a free-text field
- Changing keyboard navigation or dropdown filtering logic

## Impact

- **Code**: `TypeaheadSelect.svelte` — `handleClickOutside`, `handleKeydown` (Tab case), and the `$effect` that restores `displayText`
- **Pages affected**: Organizations (org type), Interactions (interaction type), Relationships (org/person selectors), Leads (org/person selectors), People (interaction type quick-log)
- **Specs**: `typeahead-selector` spec needs updated blur scenarios
