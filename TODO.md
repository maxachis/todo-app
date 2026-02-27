

- [ ] Should I add hints somewhere for shortcut keys on each page?
- [ ] On interactions, allow Ctrl + Up/Down to move between different elements.
- [ ] Task: Typing "Tab" or "Shift+Tab" to promote/demote a task disables keying up and down

## Regression
That 

# TODO

## Follow-Up Dashboard

Surface the `follow_up_cadence_days` field on Person in a dedicated view. Show who's overdue for contact by comparing their last interaction date against their cadence. Bridges the task and CRM halves — overdue follow-ups could auto-suggest creating a task.

## Today / Dashboard View

A single "what should I focus on right now?" page combining:
- Pinned tasks
- Tasks due today
- Overdue tasks
- Overdue follow-ups (from CRM)
- Recent interactions

One glanceable view instead of jumping between Upcoming, People, and Interactions.

## Reporting / Analytics

Leverage existing timesheet, completion, and interaction data to show trends:
- Tasks completed over time
- Time spent per project (weekly/monthly)
- Interaction frequency per contact
- Project velocity / burndown

## Tags as First-Class Navigation

Tags exist on tasks but aren't browsable. Add:
- A tag cloud or tag list view
- Filter tasks by tag across all lists
- Possibly tag-based saved filters or smart lists

## Recurring Interaction Reminders

Combine the interaction tracking system with recurring task patterns. Define repeating interaction reminders like "Call Mom every 2 weeks" — when an interaction is logged, the next reminder auto-schedules. Different from follow-up cadence in that it's explicit and action-oriented.
