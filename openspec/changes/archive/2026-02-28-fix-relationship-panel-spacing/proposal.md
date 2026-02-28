## Why

The Relationships page panels have excessive vertical spacing between form inputs when the viewport is tall relative to the content. The h2 heading, form fields (Person A, Person B, Notes), and relationship list spread out to fill available height instead of staying compact at the top.

## What Changes

- Fix CSS on `.panel` in the Relationships page to prevent grid rows from stretching to fill available space
- Form inputs and list items will stay tightly spaced regardless of viewport height

## Capabilities

### New Capabilities

_None — this is a CSS bug fix._

### Modified Capabilities

_None — no spec-level behavior changes. The layout requirements are unchanged; this fixes an implementation bug where the grid rows stretch instead of packing at the top._

## Impact

- **Frontend**: `frontend/src/routes/relationships/+page.svelte` — CSS only, one property addition
- **No backend changes**

## Non-goals

- Redesigning the Relationships page layout
- Changing spacing values between form fields
