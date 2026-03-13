## Context

The `ShortcutHints` component currently accepts a flat `shortcuts` array of `{ key, description }`. The notebook needs both keyboard shortcuts and typing syntax prompts, which are conceptually different and should be visually grouped.

## Goals / Non-Goals

**Goals:**
- Support grouped sections in the hints popover (e.g., "Shortcuts" and "Syntax")
- Keep the component backward-compatible — a flat array still works (Tasks page unchanged)
- Surface the most useful notebook typing triggers concisely

**Non-Goals:**
- Exhaustive documentation of every Markdown feature
- Interactive/tutorial-style hints

## Decisions

### 1. Add optional `sections` prop alongside existing `shortcuts` prop
The component accepts either a flat `shortcuts` array (existing behavior) or a `sections` array of `{ title, shortcuts }` groups. If `sections` is provided, it renders grouped with section headings. If only `shortcuts` is provided, it renders flat as before.

**Alternative**: Always require sections. Rejected — adds unnecessary verbosity for pages with only a few shortcuts (like Tasks).

### 2. Notebook syntax hints to include
Keep it to the triggers a user would type, not the stored format:

| Trigger | Description |
|---------|-------------|
| `@Name` | Mention a person |
| `@new[Name]` | Draft new contact |
| `[[` | Link to entity |
| `- [ ]` | Create checkbox / task |

These are the four non-obvious triggers. Markdown formatting (bold, headers, etc.) is excluded as standard knowledge.

## Risks / Trade-offs

- [Popover gets tall] → With ~5 syntax hints + 1 shortcut, it's still compact (~6 rows). Not a concern at this scale.
