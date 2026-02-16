| TODO Item | Deliverable | Manual Validation | Validated | Failure Notes |
|-----------|-------------|-------------------|-----------|---------------|
| When pinning, ensure user doesn't get disoriented because sections move down to accomodate space for new pin. | Added pin/unpin viewport anchoring so the clicked task stays visually stable after HTMX center-panel re-render. | Scroll center panel to middle of a long list, pin a non-visible-top task, and confirm the viewport does not jump to a different region after the swap. Repeat for unpin. | [ ] | Does not currently work. |
