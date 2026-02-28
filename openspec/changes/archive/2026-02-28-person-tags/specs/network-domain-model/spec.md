## ADDED Requirements

### Requirement: Person has tags via PersonTag
The Person model SHALL include a ManyToManyField to PersonTag (`tags`, blank=True, related_name="people"). PersonTag SHALL be a separate model in the network domain with a unique `name` field (CharField, max 100).

#### Scenario: Person with tags
- **WHEN** a person is created and associated with PersonTag records
- **THEN** the tags are retrievable via the person's `tags` M2M field
