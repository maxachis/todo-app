# Task Execution Instructions

Instructions for an orchestrating agent to implement the items in `TODO.md`.

## Input

`TODO.md` contains a checklist of tasks. Each line is a standalone work item. Some are code tasks, some are ops tasks, some are research/documentation tasks.

## Step 1: Classify Each Task

Read every line in `TODO.md`. For each, determine its **type**:

| Type | Description | Example |
|------|-------------|---------|
| `code` | Requires changes to application source code, templates, JS, CSS, tests, or migrations | "Add sorting" |
| `ops` | Requires server/infrastructure configuration, deployment scripts, or manual steps on the VPS | "Set up and test backup system" |
| `research` | Requires investigation and a written document as output — no code changes | "What would be needed to give it cloud support?" |

## Step 2: Identify Conflicts

Before deploying subagents in parallel, check for conflicts. Two tasks conflict if they are likely to edit the same files. Tasks that conflict must run sequentially.

**Conflict rules:**
- Two `code` tasks conflict if they touch overlapping areas (e.g., both modify `models.py`, or both change the same template). When in doubt, assume they conflict.
- A `code` task and an `ops` task generally do not conflict (different file trees: `tasks/` vs `deploy/`).
- A `research` task never conflicts with anything — it only produces new documents.
- If a task depends on another's output (e.g., "test the backup system" depends on "set up the backup system"), they must run sequentially regardless.

Build a dependency/conflict map before launching anything.

## Step 3: Deploy Subagents

For each task (or group of non-conflicting tasks in parallel), spawn a subagent with the following context:

### Subagent Prompt Template

```
You are implementing a task from the project's TODO list.

**Task:** {the original TODO line}
**Task type:** {code | ops | research}

**Project context:**
- Read `CLAUDE.md` for project conventions, structure, and commands.
- Read `SPECS.md` for functional requirements and test matrix.
- Read `plan.md` for implementation history and architecture decisions.

**Rules:**
1. Read before you write. Understand the existing code, patterns, and conventions before making changes.
2. Follow the code style and architecture in `CLAUDE.md` exactly.
3. For `code` tasks: run `python manage.py test tasks` after implementation. All tests must pass.
4. For `code` tasks involving model changes: run `python manage.py makemigrations && python manage.py migrate`.
5. For `ops` tasks: note which steps require manual action by the operator (SSH, credentials, dashboard logins) and which can be scripted. Only implement the scriptable parts. Document the manual parts clearly.
6. For `research` tasks: produce a Markdown document at the project root. Be concrete and specific to this project's stack — no generic advice.
7. Do not modify files outside your task's scope. If you discover something that needs fixing elsewhere, note it but do not change it.
8. When done, fill in the tracking table (format below) with what you implemented and how the operator can manually verify each deliverable.
```

### File Boundaries

To prevent subagents from stepping on each other, assign explicit file boundaries when deploying parallel tasks:

- **Code tasks** own: `tasks/`, `static/`, `templates/`, and migration files they create.
- **Ops tasks** own: `deploy/`, and any new config/doc files in the project root related to deployment.
- **Research tasks** own: only the specific output document they create (e.g., `CLOUD-SUPPORT.md`).

If two code tasks must run in parallel (rare), partition by file. For example: "Task A may only modify `tasks/models.py`, `tasks/views/`, and `tasks/tests/`" vs "Task B may only modify `static/` and `templates/`". Spell this out in each subagent's prompt.

## Step 4: Collect Results into Tracking Table

Each subagent returns a filled-in tracking table. The orchestrator merges them into `VALIDATION.md` using this format:

```markdown
| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| Original text from TODO.md | What was implemented or produced | Steps for the human to verify | [ ] | |
```

**Column definitions:**

- **TODO Item**: The original line from `TODO.md`. First row per task shows the text; subsequent rows for the same task leave this blank (merged cell style).
- **Deliverable**: A specific, concrete thing the subagent produced. One row per deliverable. Be granular — "added sort dropdown to UI" is better than "implemented sorting". Each row should be independently verifiable.
- **Manual Validation**: Exact steps the human should take to verify this deliverable works. Include specific commands to run, pages to visit, or things to look for. The human should be able to follow these without reading the code.
- **Validated**: `[ ]` initially. The human checks `[x]` after verifying. Rows that pass are removed from the table.
- **Failure Notes**: Filled in by the human during validation. Describes the observed behavior when a deliverable fails — what actually happened vs. what was expected. This column is the primary input for fix-up iterations: the agent reads it to understand what went wrong without needing a back-and-forth conversation. Be specific ("badge count doesn't update until page refresh") not vague ("doesn't work").

**Guidelines for good deliverable rows:**
- Each row should test one thing. Don't combine "sort by priority works AND sort by title works" into one row.
- Validation steps should be concrete: "Select 'Priority' from the sort dropdown on any list — tasks with High priority appear before Low" not "verify sorting works."
- For ops tasks, include both automated checks (`systemctl status ...`) and manual checks (dashboard screenshots, data spot-checks).
- For research tasks, validation is about completeness: "Document covers authentication options with at least 3 approaches compared."

**Fix-up workflow:** After the human fills in failure notes, the orchestrator reads `VALIDATION.md`, groups failures by file/area, and deploys subagents to fix them — following the same conflict rules as initial implementation. Fixed rows go through validation again.

## Step 5: Update TODO.md and VALIDATION.md

After all subagents complete and the human has validated:
- Check off completed items in `TODO.md`: `- [ ]` becomes `- [x]`
- Remove items the human confirms are done
- Add any new items discovered during implementation
- Keep `VALIDATION.md` as the living record — validated rows stay as a log of what was verified and when

## Notes

- **Test isolation:** If multiple code subagents run in parallel and both need to run tests, they may collide on the test database. Either run tests sequentially after all code changes are done, or ensure each subagent only runs tests related to their changes.
- **Migration ordering:** Only one subagent at a time should create migrations. If two code tasks both require model changes, run them sequentially or have the second subagent create its migration after the first's is applied.
- **Git:** Subagents should not commit. The human reviews all changes and commits after validation.
