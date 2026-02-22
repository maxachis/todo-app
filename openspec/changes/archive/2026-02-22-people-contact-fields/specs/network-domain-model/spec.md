## ADDED Requirements

### Requirement: Person has email and LinkedIn contact fields
The Person model SHALL include an optional `email` field (CharField, max 255, blank) and an optional `linkedin_url` field (CharField, max 500, blank) for storing contact information.

#### Scenario: Create person with email and LinkedIn
- **WHEN** a person is created with `email` set to "jane@example.com" and `linkedin_url` set to "https://linkedin.com/in/jane"
- **THEN** both values are persisted on the person record

#### Scenario: Create person without contact fields
- **WHEN** a person is created without providing `email` or `linkedin_url`
- **THEN** both fields default to empty strings

#### Scenario: Update person contact fields
- **WHEN** a person's `email` or `linkedin_url` is updated
- **THEN** the new values are persisted and the `updated_at` timestamp changes
