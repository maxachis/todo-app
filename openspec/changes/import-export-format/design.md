## Context

The app exports task data in three formats via `tasks/views/export.py`:
- **JSON**: Nested hierarchy (`list > sections > tasks > subtasks`) with fields: `title`, `notes`, `due_date`, `is_completed`, `completed_at`, `position`, `tags`, `subtasks`.
- **CSV**: Flat rows with columns: `list`, `section`, `task`, `parent_task`, `depth`, `notes`, `due_date`, `tags`, `is_completed`.
- **Markdown**: Human-readable, not structured for re-import.

The current import endpoint (`POST /api/import/`) only accepts TickTick CSV files via `tasks/services/ticktick_import.py`. It uses TickTick-specific columns (`taskId`, `parentId`, `List Name`, `Column Name`) and handles a metadata preamble.

The frontend import page (`frontend/src/routes/import/+page.svelte`) only accepts `.csv` files and labels itself "Import tasks from a TickTick CSV export."

## Goals / Non-Goals

**Goals:**
- Accept the app's own JSON export files via `POST /api/import/` and reconstruct full list/section/task/subtask hierarchies.
- Accept the app's own CSV export files via `POST /api/import/` and reconstruct tasks with parent relationships using the `parent_task` + `depth` columns.
- Auto-detect the import format (native JSON, native CSV, TickTick CSV) without requiring the user to specify it.
- Return the same `ImportSummary` response shape for all import formats.
- Update the frontend import page to accept `.json` files and describe all supported formats.

**Non-Goals:**
- Importing Markdown exports (lossy format, not structured for round-tripping).
- Changing the existing export format or adding new export fields.
- Merging/conflict resolution — importing creates new records; duplicates are handled by title matching within the same list/section context, not by ID.

## Decisions

### 1. Format auto-detection strategy

**Decision**: Detect format by file extension first, then validate content structure.

- `.json` → parse as JSON, validate it matches the export schema (array of lists or single list object with `name` and `sections` keys).
- `.csv` → read the header row. If it contains `taskId` and `Title`, route to existing TickTick importer. If it contains `list`, `section`, `task`, route to native CSV importer.

**Why**: File extension is the simplest reliable signal. Header-based detection for CSV disambiguates between native and TickTick formats without requiring the user to label the file. This avoids adding a format parameter to the API.

**Alternative considered**: Requiring a `format` query parameter on the endpoint. Rejected because it adds friction and the formats are unambiguously distinguishable.

### 2. Duplicate handling for native imports

**Decision**: Use title-based matching within (list, section) scope. If a list+section+task title combination already exists, skip the task and report it as skipped.

**Why**: Unlike TickTick imports which have `external_id` for idempotency, the native export format has no stable ID. Title matching within the same structural context is the most intuitive behavior for re-importing your own data.

**Alternative considered**: Always creating new records (no dedup). Rejected because re-importing an export should be safe to repeat.

### 3. Service module organization

**Decision**: Create a single new module `tasks/services/native_import.py` with two public functions: `import_native_json(file)` and `import_native_csv(file)`. The API router (`tasks/api/import_tasks.py`) handles detection and dispatching.

**Why**: Keeps the import logic cleanly separated by format, paralleling the existing `ticktick_import.py` module. The API layer stays thin — just detection and dispatch.

### 4. Subtask reconstruction from CSV

**Decision**: Use the `parent_task` column (parent title) combined with `depth` to reconstruct parent-child relationships. Within a section, find the most recent task at `depth - 1` with the matching title.

**Why**: The CSV export includes both `parent_task` (parent's title) and `depth` (nesting level). Together these are sufficient to reconstruct the tree. The export writes tasks in depth-first order, so the parent always precedes its children.

### 5. Frontend changes

**Decision**: Minimally update the import page:
- Change `accept=".csv"` to `accept=".csv,.json"`.
- Update the description text to list all supported formats.
- No format selector needed — the backend auto-detects.

**Why**: The auto-detection approach means the frontend doesn't need to know about formats. The user just picks a file.

## Risks / Trade-offs

- **[Title-based dedup may mis-match]** → If a user has multiple tasks with identical titles in the same section, re-import could incorrectly skip them. Mitigation: this is an edge case for a single-user app; documented as known behavior.
- **[CSV parent resolution is positional]** → If the exported CSV is manually reordered, parent-child linking could break. Mitigation: document that CSV files should not be manually reordered before re-import. JSON format is recommended for reliable round-tripping.
- **[No completed_at in CSV export]** → The native CSV format doesn't include `completed_at`. Mitigation: accept this data loss for CSV import; JSON import preserves all fields. Users who need full fidelity should use JSON.
