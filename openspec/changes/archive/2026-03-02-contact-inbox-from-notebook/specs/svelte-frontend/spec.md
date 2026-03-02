## MODIFIED Requirements

### Requirement: CRM sub-tab navigation
The CRM layout SHALL display sub-tabs in the order: **Inbox**, People, Orgs, Interactions, Leads. The Inbox tab SHALL link to `/crm/inbox`. The Inbox tab SHALL display a count badge showing the number of pending contact drafts (non-promoted, non-dismissed). The badge SHALL be hidden when the count is zero.

#### Scenario: CRM tabs include Inbox first
- **WHEN** the user navigates to any `/crm/*` route
- **THEN** the sub-tabs display in order: Inbox, People, Orgs, Interactions, Leads

#### Scenario: Inbox badge shows pending count
- **WHEN** there are 3 pending contact drafts
- **THEN** the Inbox tab displays "Inbox (3)" or a numeric badge next to the label

#### Scenario: Inbox badge hidden when empty
- **WHEN** there are no pending contact drafts
- **THEN** the Inbox tab displays "Inbox" with no badge

## ADDED Requirements

### Requirement: CRM Inbox page
The system SHALL provide a `/crm/inbox` route displaying pending contact drafts in a two-panel layout matching the existing CRM pattern: a list of drafts (left) and a triage detail panel (right). The `/crm` root route SHALL redirect to `/crm/inbox` instead of `/crm/people`.

#### Scenario: Inbox loads with pending drafts
- **WHEN** the user navigates to `/crm/inbox` with pending drafts
- **THEN** the left panel shows a list of drafts with name and quick notes preview, ordered by most recent first

#### Scenario: Inbox empty state
- **WHEN** the user navigates to `/crm/inbox` with no pending drafts
- **THEN** the page shows an empty state message (e.g., "No contacts to triage. Use @new[Name] in notebook pages to capture contacts.")

#### Scenario: Select a draft shows triage detail
- **WHEN** the user clicks a draft in the list
- **THEN** the right panel shows the draft's name, full quick notes, source page link, match hints (if any), and action buttons

### Requirement: Triage detail panel
The triage detail panel SHALL display: the draft name (as heading), quick notes (as body text), source page (as clickable link to `/notebook/{slug}`), match hints (people and org matches from the API), and action buttons. The action buttons SHALL be: "→ Person" (opens promotion form for Person), "→ Org" (opens promotion form for Organization), and "Dismiss" (dismisses the draft).

#### Scenario: Source page link navigates to notebook
- **WHEN** the user clicks the source page link in the triage detail
- **THEN** the app navigates to `/notebook/{source_page_slug}`

#### Scenario: Match hints displayed
- **WHEN** a draft is selected and the matches API returns existing people or orgs
- **THEN** the detail panel shows a "Possible matches" section listing each match with a "Link to [Name]" button

#### Scenario: No match hints
- **WHEN** a draft is selected and the matches API returns empty arrays
- **THEN** no "Possible matches" section is shown

### Requirement: Promote to Person form
Clicking "→ Person" in the triage detail SHALL display an inline form pre-filled from the draft. The first token of the draft name SHALL pre-fill `first_name`, the remaining tokens SHALL pre-fill `last_name`. The `notes` field SHALL pre-fill with the draft's `quick_notes`. Additional optional fields SHALL be shown: `middle_name`, `email`, `linkedin_url`, `follow_up_cadence_days`. The form SHALL submit to the promote-to-person API endpoint. On success, the draft disappears from the list and the next pending draft (if any) is auto-selected.

#### Scenario: Name split pre-fill
- **WHEN** the user clicks "→ Person" for a draft named "Jane Smith"
- **THEN** the form shows `first_name="Jane"` and `last_name="Smith"`

#### Scenario: Multi-word name split
- **WHEN** the user clicks "→ Person" for a draft named "Mary Jane Watson"
- **THEN** the form shows `first_name="Mary"` and `last_name="Jane Watson"` (first token vs rest)

#### Scenario: Quick notes pre-fill
- **WHEN** the draft has `quick_notes="works at Stripe"`
- **THEN** the notes field is pre-filled with "works at Stripe"

#### Scenario: Successful promotion
- **WHEN** the user fills in required fields and submits the Person form
- **THEN** the draft is promoted, removed from the inbox list, and the next draft is selected

#### Scenario: Duplicate person name error
- **WHEN** the user submits a Person form with a name that already exists (409 from API)
- **THEN** an error toast is shown and the form remains open

### Requirement: Promote to Organization form
Clicking "→ Org" in the triage detail SHALL display an inline form pre-filled from the draft. The `name` field SHALL pre-fill with the full draft name. The `org_type` field SHALL use a TypeaheadSelect with inline creation (matching the existing Orgs page pattern). The `notes` field SHALL pre-fill with the draft's `quick_notes`. The form SHALL submit to the promote-to-org API endpoint.

#### Scenario: Org form pre-fill
- **WHEN** the user clicks "→ Org" for a draft named "Acme Corp"
- **THEN** the form shows `name="Acme Corp"` and `notes` pre-filled from quick_notes

#### Scenario: Org type required
- **WHEN** the user submits the Org form without selecting an org type
- **THEN** validation prevents submission (org type is required)

#### Scenario: Inline org type creation
- **WHEN** the user types a new org type name in the TypeaheadSelect
- **THEN** an inline creation option appears, matching the existing Orgs page behavior

### Requirement: Link to existing record
Clicking "Link to [Name]" on a match hint SHALL call the link API endpoint, skipping the promotion form entirely. On success, the draft is removed from the inbox list.

#### Scenario: Link to existing person
- **WHEN** the user clicks "Link to Jane Smith" on a person match hint
- **THEN** the draft is linked to the existing Person, quick notes are appended to the person's notes, and the draft is removed from the inbox list

#### Scenario: Link to existing org
- **WHEN** the user clicks "Link to Acme Corp" on an org match hint
- **THEN** the draft is linked to the existing Organization and removed from the inbox list

### Requirement: Dismiss action
Clicking "Dismiss" SHALL call the dismiss API endpoint and remove the draft from the inbox list. The next pending draft (if any) SHALL be auto-selected.

#### Scenario: Dismiss a draft
- **WHEN** the user clicks "Dismiss"
- **THEN** the draft is dismissed via API and removed from the list

#### Scenario: Dismiss last draft shows empty state
- **WHEN** the user dismisses the last pending draft
- **THEN** the inbox shows the empty state message
