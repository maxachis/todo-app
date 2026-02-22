## Context

The Outlook email import feature was added in commit `89e225b` to poll Microsoft Graph API for emails tagged with a configurable category and import them as tasks. Testing revealed that Graph API only accesses the Microsoft mailbox, not Gmail accounts linked via IMAP in the Outlook desktop client. Since the user's primary email is Gmail, the feature is non-functional and should be cleanly removed.

The feature touched: backend services, management commands, API endpoint, frontend layout, Django settings, Python dependencies, deploy config, and deploy helper scripts.

## Goals / Non-Goals

**Goals:**
- Completely remove all Outlook integration code and configuration
- Restore `pyproject.toml` dependencies to pre-Outlook state
- Keep the `run-manage.sh` deploy helper (useful independent of Outlook)
- Preserve the expanded emoji picker (shipped in the same commit but unrelated)
- Leave core file import (JSON/CSV) fully intact

**Non-Goals:**
- Building an alternative email import mechanism (separate future change)
- Modifying the devcontainer SSH mount (added in same commit but independently useful)

## Decisions

### 1. Full removal over feature-flagging
Remove all Outlook code rather than disabling it behind a flag. The feature is architecturally incompatible with the user's email setup (Gmail via IMAP in Outlook), not just misconfigured. There's no value in keeping dead code.

### 2. Keep `run-manage.sh`, remove Outlook-specific scripts
`deploy/run-manage.sh` is a general-purpose helper for running manage.py with `.env` loaded — useful for any management command. `outlook-whoami.sh` and `outlook-debug.sh` are Outlook-specific and should be removed.

### 3. Remove `html2text` and `msal` dependencies, keep `requests` if needed elsewhere
Check whether `requests` is used by any other code before removing. `msal` and `html2text` were added solely for the Outlook feature.

### 4. Archive the `outlook-email-import` change directory
Remove `openspec/changes/outlook-email-import/` since the feature is being fully reverted.

## Risks / Trade-offs

- **[Risk] Server has leftover files** → Document that `outlook_token_cache.json`, `outlook_poll_status.json`, and any crontab entry should be manually cleaned up on the production server.
- **[Risk] `requests` used elsewhere** → Verify before removing from `pyproject.toml`. If used, keep it.
- **[Risk] Lock file churn** → Removing three dependencies will change `uv.lock` significantly, but this is expected and correct.
