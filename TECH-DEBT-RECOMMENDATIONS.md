# Tech Debt Recommendations

Actionable items to reduce friction for future development, ordered by impact.

## 1. Split `app.js` into modules

**Problem:** `static/js/app.js` is a single file handling 7+ concerns: SortableJS init, keyboard navigation, toast management, emoji picker, markdown editor, completion transitions, and focus tracking. Every JS-related task requires reading the full file, and parallel agents cannot work on JS features simultaneously.

**Fix:** Split into separate files by concern:

```
static/js/
  sortable.js          # SortableJS init for tasks, sections, lists
  keyboard.js          # All keyboard navigation and shortcuts
  toast.js             # Toast display, dismiss, auto-timeout
  emoji-picker.js      # Emoji picker modal
  markdown-editor.js   # Live markdown block editor
  completion.js        # Check-off transitions and optimistic UI
  focus.js             # Focus tracking and restoration after HTMX swaps
  app.js               # Imports/init: calls initAll() from each module
```

Each file owns one concern. `app.js` becomes a thin orchestrator that calls `initSortable()`, `initKeyboardNav()`, etc. on `DOMContentLoaded` and `htmx:afterSwap`.

**Effort:** Medium. No behavior change — just file splitting and adding `<script>` tags to `base.html`. No build step needed (vanilla JS, no bundler).

**Unblocks:** Parallel agent work on any JS feature. Two agents can edit `keyboard.js` and `sortable.js` simultaneously with zero conflict risk.

## 2. Add integration tests for client-server flows

**Problem:** Automated tests (`python manage.py test tasks`) only cover Django views and models. They don't test the JS → fetch → Django → DOM update pipeline. Every drag-drop and keyboard shortcut bug has required multiple manual validation rounds because the test suite can't catch them.

**Fix:** Add a small Playwright or Selenium test suite for critical interactive flows:

- Drag-and-drop: reorder tasks, sections, lists → refresh → verify order persisted
- Task completion: check off → verify toast appears → click undo → verify task restored
- Keyboard nav: arrow keys, Tab indent, Delete key
- Search: type query → verify results → click result → verify navigation

**Effort:** Medium-high. Requires adding a test dependency (Playwright is already referenced in `.devcontainer/Dockerfile`). Start with 5-10 tests covering the flows that have broken repeatedly.

**Unblocks:** Agents can verify their JS changes actually work end-to-end before declaring done.

## 3. Use OOB swaps consistently instead of full panel replacement

**Problem:** Many views still return full `#center-panel` innerHTML swaps. This causes:
- Flicker from CSS animations replaying on new elements
- SortableJS instances being destroyed and needing reinitialization
- Loss of scroll position, focus state, and `<details>` open/closed state

The flicker fix (round 3) demonstrated the correct pattern: `hx-swap="none"` on the trigger element, with the server returning targeted OOB swap fragments.

**Fix:** Audit all HTMX-driven views and migrate from `hx-target="#center-panel" hx-swap="innerHTML"` to OOB swaps where possible. Priority targets:
- Task create/delete (currently re-renders full panel)
- Section create/delete
- Tag add/remove

**Effort:** Medium per view. The `complete_task`/`uncomplete_task` views are already converted and can serve as the pattern.

**Unblocks:** Smoother UX across the board. Eliminates a whole class of "flicker" and "state lost after action" bugs.

## 4. Reinitialize SortableJS on targeted HTMX swaps

**Problem:** HTMX swaps replace DOM elements, destroying attached SortableJS instances. The current `initSortable()` function tears down ALL instances and rebuilds ALL of them on every swap. This is wasteful and causes the "lag after section drag" issue — a single section move triggers reinitialization of every sortable on the page.

**Fix:** Instead of a global `destroySortables()` + `initSortable()` cycle:
- Track which DOM elements have Sortable instances (via a WeakMap or data attribute)
- On `htmx:afterSwap`, only initialize Sortable on NEW elements that don't already have an instance
- On `htmx:beforeSwap`, only destroy instances on elements that are about to be replaced

**Effort:** Low-medium. Mostly refactoring `initSortable()`.

**Unblocks:** Eliminates post-drag lag. Makes sidebar OOB swaps safe (won't destroy center panel sortables).

## 5. Standardize the move/reorder view pattern

**Problem:** `move_task`, `move_section`, and `move_list` were implemented at different times and use slightly different position-calculation logic. The section and list move views have been rewritten twice due to bugs in position renumbering.

**Fix:** Extract a shared utility:

```python
def reorder_siblings(instance, queryset, new_index):
    """Move `instance` to `new_index` within `queryset` and renumber all with gap-based positions."""
    siblings = list(queryset.exclude(pk=instance.pk).order_by("position"))
    siblings.insert(new_index, instance)
    for i, obj in enumerate(siblings):
        obj.position = i * 10
        obj.save(update_fields=["position"])
```

Use this in all three move views. One tested function, one behavior.

**Effort:** Low. Pure refactoring.

**Unblocks:** Future reorderable entities (e.g., tags) get correct behavior for free.

## 6. Update `TASK-EXECUTION-INSTRUCTIONS.md` with lessons learned

**Problem:** The instructions allow parallel agents on the same file if they touch "different sections." In practice, this caused conflicts and stale reads on `app.js`.

**Fix:** Add stricter rules:
- **Never parallelize agents that write to the same file**, regardless of which section they edit
- **Require a test-suite run between sequential agents** that share files, to catch conflicts early
- **For JS changes, require a browser smoke test** (manual or Playwright) in addition to Django tests
- **For recurring failures (3+ rounds), escalate** — have the agent read the previous failure notes and propose a fundamentally different approach, not an incremental fix

**Effort:** Low. Documentation update.
