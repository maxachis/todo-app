## MODIFIED Requirements

### Requirement: Live Markdown editor
The system SHALL provide a block-based Markdown editor for task notes. Inactive blocks SHALL show rendered HTML; the active block SHALL show raw Markdown. The editor SHALL provide visual affordances indicating that content is editable.

#### Scenario: Click to edit a block
- **WHEN** the user clicks a rendered Markdown block in the notes area
- **THEN** that block switches to a raw Markdown textarea for editing

#### Scenario: Blur saves and renders
- **WHEN** the user blurs the active Markdown block
- **THEN** the block saves via API and renders back to HTML

#### Scenario: Supported Markdown syntax
- **WHEN** the user writes Markdown using headings, bold, italic, strikethrough, inline code, lists, blockquotes, code fences, or horizontal rules
- **THEN** the rendered output displays the correct HTML formatting

#### Scenario: XSS sanitization
- **WHEN** task notes contain script tags or event handler attributes
- **THEN** the rendered HTML strips all dangerous content

#### Scenario: Empty notes placeholder
- **WHEN** the notes field has no content
- **THEN** the editor SHALL display a muted placeholder text "Click to add notes..." that invites interaction
- **AND** clicking the placeholder SHALL open the editor textarea for that block

#### Scenario: Hover edit affordance on rendered blocks
- **WHEN** the user hovers over a rendered Markdown block that has content
- **THEN** a small pencil icon SHALL appear in the top-right corner of the block to indicate editability
- **AND** the block border and background SHALL become visible to reinforce interactivity

#### Scenario: Keyboard accessibility of edit affordance
- **WHEN** a rendered Markdown block receives keyboard focus
- **THEN** the same visual affordance (border, background) SHALL appear as on hover
