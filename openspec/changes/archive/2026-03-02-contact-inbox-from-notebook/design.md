## Context

The app has a notebook (daily/wiki pages with mention syntax) and a CRM (people, organizations, interactions, leads). There's no quick-capture path from notes to CRM records — users must switch to the CRM view and fill in full forms. The notebook already has a `reconcile_mentions` function that parses content on save to sync mention records and create tasks from `- [ ]` checkboxes, so extending it to detect a new `@new[...]()` syntax and create contact drafts is architecturally natural.

People require `first_name` + `last_name`. Organizations require `name` + `org_type` (FK). These required fields make instant record creation from freeform text impractical — a staging model is needed.

## Goals / Non-Goals

**Goals:**
- `@new[Name](optional notes)` syntax in notebook content that creates ContactDraft records on save
- ContactDraft model as lightweight staging area (name + notes, no required relational fields)
- CRM Inbox tab (first tab) for triaging drafts into People or Organizations
- Promotion flow: pre-filled forms for Person or Org creation, with quick notes migrating to the notes field
- Match hints: when a draft name resembles an existing Person or Org, surface a "link to existing" option
- Notebook content rewrite on promotion: `@new[Name](notes)` → `@[person:ID|Name]` or `[[org:ID|Name]]`

**Non-Goals:**
- Deduplication at capture time (two `@new[Jane Smith]` on different pages = two drafts)
- Auto-classification of person vs org at capture (user decides at triage)
- Bidirectional sync after promotion (name changes on the record don't update notebook text)
- Merging duplicate drafts in the inbox
- Creating relationships or interactions from the inbox (triage produces only a Person or Org)
- Bulk triage actions (one at a time is fine for now)

## Decisions

### 1. ContactDraft model with two nullable FKs

**Decision**: Add `ContactDraft` to `network/models/` with fields: `name` (str), `quick_notes` (text), `source_page` (FK → Page), `promoted_to_person` (nullable FK → Person), `promoted_to_org` (nullable FK → Organization), `dismissed` (bool), `created_at`.

**Why over alternatives**:
- *Generic FK (type + id)*: Requires ContentType framework or manual type dispatching. The codebase already uses separate link models (`TaskPerson`, `TaskOrganization`) rather than polymorphic FKs — two nullable FKs is consistent.
- *Separate PersonDraft/OrgDraft models*: The whole point is that classification happens at triage, not capture. A single model avoids premature type commitment.
- *No model (parse on demand)*: Drafts need state — promoted, dismissed, or pending. A model makes this queryable and the inbox UI straightforward.

**Constraints**: At most one of `promoted_to_person` / `promoted_to_org` can be non-null. Enforced at application level (promotion endpoint sets one, clears the other). A draft is "pending" when both are null and `dismissed=False`.

### 2. `@new[Name](notes)` syntax parsed in `reconcile_mentions`

**Decision**: Add a new regex to `notebook/mentions.py` matching `@new\[([^\]]+)\](?:\(([^)]*)\))?`. On page save, `reconcile_mentions` runs this regex. For each match where no ContactDraft with the same `name` and `source_page` already exists, a new ContactDraft is created. The page content is NOT rewritten at capture time — the `@new[...]` text remains until promotion.

**Why over alternatives**:
- *Rewrite at capture time*: There's nothing to rewrite TO yet — we don't have an entity ID until promotion. Keeping `@new[...]` in the content also serves as a visual reminder that triage is pending.
- *Frontend-side detection*: Same reasoning as checkbox-to-task — server-side keeps it atomic and avoids race conditions.
- *Deduplicate by name across pages*: Would require `@new[Jane Smith]` on page B to discover the draft from page A. This adds complexity and could silently link unrelated people with the same name. Per-page drafts are simpler; the inbox shows them all and the user decides.

**Idempotency**: Re-saving a page with an existing `@new[Jane Smith]` should NOT create a duplicate draft for that page. The check is `ContactDraft.objects.filter(name=name, source_page=page).exists()`.

### 3. Promotion rewrites all matching notebook pages

**Decision**: When a draft is promoted to Person #42 (or linked to existing Person #42), the system finds all pages containing `@new[Jane Smith]` (with or without parenthetical notes) and rewrites them to `@[person:42|Jane Smith]`. For organizations, rewrites to `[[org:42|Jane Smith]]`. The quick notes parenthetical is stripped — those notes have migrated to the record's notes field.

**Rewrite regex**: `@new\[Jane Smith\](?:\([^)]*\))?` — escaped name, optional parenthetical. Applied to all pages, not just `source_page`, since the same name may appear on multiple pages.

**Note accumulation**: When multiple drafts exist for the same name (from different pages), promoting one should prompt about the others. The promotion endpoint handles one draft at a time, but the page rewrite sweeps all content. Remaining drafts for the same name can be auto-dismissed after promotion since their notebook references have been rewritten.

### 4. CRM Inbox as first tab

**Decision**: Add "Inbox" as the first tab in the CRM layout (`/crm/inbox`), before People. The tab shows a count badge of pending drafts. The UI is a two-panel layout matching the existing CRM pattern: list of pending drafts (left), triage detail (right).

**Why first tab**: Mirrors the task Inbox-first pattern. The inbox is where you start when triaging — it should be immediately visible.

**Triage detail panel** shows:
- Draft name and quick notes
- Source page link (clickable, navigates to notebook page)
- Match hints (if existing Person or Org name-matches)
- Action buttons: "→ Person", "→ Org", "→ Link to [existing]", "Dismiss"

### 5. Match hints via fuzzy name search

**Decision**: When a draft is selected in the inbox, the frontend queries a match-hints endpoint: `GET /api/network/contact-drafts/:id/matches/`. The backend searches for People by `first_name + last_name` and Organizations by `name`, using case-insensitive containment. Results are shown as clickable hints above the action buttons.

**Why server-side matching**: Person names are split into first/last. A draft name "Jane Smith" needs to check `first_name__iexact="Jane", last_name__iexact="Smith"` but also handle cases like "Jane M. Smith" where the middle name is included. A simple split-on-spaces heuristic (first token → first_name, last token → last_name) is sufficient; exact matching catches most cases and the user can always manually promote.

**Matching strategy**:
- People: Split draft name on whitespace. First token → `first_name__iexact`, last token → `last_name__iexact`. Also check `first_name__icontains` OR `last_name__icontains` with each token for fuzzy results.
- Organizations: `name__icontains` on the full draft name.

### 6. Promotion form pre-fills from draft

**Decision**: Clicking "→ Person" opens an inline form (in the triage detail panel) pre-filled with:
- `first_name`: First token of draft name
- `last_name`: Remaining tokens of draft name
- `notes`: Draft's `quick_notes`

All other Person fields (email, linkedin, tags, cadence) are optional and shown empty. The form submits to the existing `POST /api/network/people/` endpoint, then calls the promotion endpoint to finalize.

For "→ Org", the form shows:
- `name`: Full draft name
- `org_type`: Required, uses TypeaheadSelect with inline creation (same as the existing Orgs page)
- `notes`: Draft's `quick_notes`

**"→ Link to [existing]"** skips the form entirely — calls the promotion endpoint with the existing record's ID, appends quick_notes to the existing record's notes (with a newline separator if notes already exist).

## Risks / Trade-offs

- **[Multi-page rewrite on promotion]** → Promotion rewrites all pages containing `@new[Name]`. If Name contains regex-special characters (parentheses, brackets), the rewrite regex needs proper escaping. **Mitigation**: Use `re.escape(name)` when constructing the rewrite pattern.

- **[Name splitting heuristic]** → Splitting "Jane Smith" into first/last is easy, but "Mary Jane Watson" is ambiguous (first="Mary Jane" or first="Mary"?). **Mitigation**: Pre-fill with first-token / rest split, but make both fields editable. User adjusts during promotion.

- **[Orphaned drafts]** → If a user removes `@new[Name]` from a page without promoting, the draft remains in the inbox with no notebook reference. **Mitigation**: Acceptable — the inbox shows all pending drafts regardless. User can dismiss stale ones manually.

- **[Quick notes appended to existing record]** → "Link to existing" appends quick_notes to the person/org notes field. If notes already contain significant content, the append could feel cluttered. **Mitigation**: Append with a clear separator (`\n---\n` + date + source page reference).

## Open Questions

None — all decisions resolved during exploration.
