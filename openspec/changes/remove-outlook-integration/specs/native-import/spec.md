## REMOVED Requirements

### Requirement: Outlook poll status endpoint
**Reason**: The Outlook email import feature is being removed because Microsoft Graph API cannot access Gmail accounts linked via IMAP in the Outlook desktop client, making the feature non-functional.
**Migration**: No migration needed. The `/import/outlook/status/` endpoint had no external consumers. The frontend status check in `+layout.svelte` is also being removed.
