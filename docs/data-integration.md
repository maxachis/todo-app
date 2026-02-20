# Data Integration: Network App → Unified ToDo DB

This document defines the **repeatable backup and import checklist** for merging the network app data into the unified ToDo database.

## Backup Locations

- ToDo DB: `db.sqlite3`
- Network DB: `import/network-app/src/db.sqlite3`
- Backup output root: `backups/` (create per-run subfolder)

Recommended per-run folder:
- `backups/unify-network-into-todo/YYYYMMDD-HHMM/`

## Backup Commands

From repo root:

```bash
# 0) Create backup folder
mkdir -p backups/unify-network-into-todo/$(date +%Y%m%d-%H%M)
BACKUP_DIR=backups/unify-network-into-todo/$(date +%Y%m%d-%H%M)

# 1) Raw DB copies
cp db.sqlite3 "$BACKUP_DIR/todo-db.sqlite3"
cp import/network-app/src/db.sqlite3 "$BACKUP_DIR/network-db.sqlite3"

# 2) JSON exports via dumpdata
# ToDo app data
uv run python manage.py dumpdata --indent 2 \
  tasks > "$BACKUP_DIR/todo-dump.json"

# Network app data
# Run from network app folder so settings are resolved correctly
cd import/network-app/src
python manage.py dumpdata --indent 2 \
  network > "$BACKUP_DIR/network-dump.json"
cd -
```

Notes:
- Use `uv run` for the ToDo app (matches project tooling).
- Network app uses its own virtualenv under `import/network-app/.venv`. Activate it if needed before running `python manage.py dumpdata`.

## Import Checklist (Repeatable)

1. **Confirm backups exist**
   - `todo-db.sqlite3`, `network-db.sqlite3`, `todo-dump.json`, `network-dump.json`

2. **Ensure unified schema exists**
   - Network app models and bridge models are present in the ToDo project.
   - Migrations are created and applied:
     ```bash
     uv run python manage.py makemigrations
     uv run python manage.py migrate
     ```

3. **Load network data into the unified DB**
   - From repo root:
     ```bash
     uv run python manage.py loaddata "$BACKUP_DIR/network-dump.json"
     ```

4. **Verify record counts**
   - Check counts for people, orgs, interactions, and relationships.
   - Verify data presence in the UI (People/Organizations/Interactions pages).

5. **Smoke test API + UI**
   - Run API endpoints:
     - `/api/people/`, `/api/organizations/`, `/api/interactions/`
   - Confirm Svelte pages render the imported data.

## Rollback

- Restore raw DB copy:
  ```bash
  cp "$BACKUP_DIR/todo-db.sqlite3" db.sqlite3
  ```

- Re-run migrations if needed after restoring.
