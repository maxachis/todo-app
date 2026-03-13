## Context

Two relationship pages exist:
- `/crm/relationships/+page.svelte` — side-by-side grid with Person↔Person and Org→Person panels, no Org↔Org
- `/network/relationships/+page.svelte` — tabbed layout with all three relationship types (Person↔Person, Org→Person, Org↔Org)

The network version is the superset. The CRM layout already links to `/crm/relationships`. The network version is unreachable via navigation.

## Goals / Non-Goals

**Goals:**
- Single relationships page at `/crm/relationships` with all three relationship types
- Tabbed sub-navigation within the page (matching the network version's pattern)
- Remove the orphaned `/network/relationships` route

**Non-Goals:**
- Refactoring the page into smaller components
- Changing the API or data model
- Adding sub-tabs to the Network layout

## Decisions

**1. Copy network version over CRM version (not merge)**

The network version (`/network/relationships/+page.svelte`) is a strict superset of the CRM version — it has the same Person↔Person and Org→Person panels plus Org↔Org, with a cleaner tabbed layout. Rather than merging features between the two, replace the CRM file with the network file contents.

Alternative: Merge Org↔Org into the existing CRM grid layout. Rejected because the tabbed approach scales better and the network version already works.

**2. Keep internal sub-tabs (not side-by-side grid)**

The network version uses `Person ↔ Person | Org → Person | Org ↔ Org` tabs within the page. This avoids horizontal scrolling on narrow screens and keeps each relationship type focused.

## Risks / Trade-offs

- **Losing the side-by-side view**: The CRM version shows Person↔Person and Org→Person simultaneously. The tabbed version shows one at a time. This is a UX trade-off favoring mobile usability and adding Org↔Org without cramming three panels. → Accept; tabs are the established pattern in the network version.
- **Duplicate code between the two files**: Both files share ~80% of their logic. During the transition there's no risk since we're replacing one with the other, not maintaining both. → No mitigation needed.
