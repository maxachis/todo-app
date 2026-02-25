- [ ] Add more emojis
- [ ] Finish setting up docker files. 
- [ ] What if you could automatically pick up emails from outlook and associate them with specific contacts?
- [ ] What if you could mark certain emails to check for follow-up later?
- [ ] Be able to add Project Links with short descriptors for each -- one-to-many relationship between project and project links
- [ ] We need a cleaner interface for associating tasks in Timesheet (for one, it's hard to see what is and is not a task, subtask, or subsubtask) -- and we need the option of linking multiple tasks at once. 
- [ ] Additionally, in Timesheet, I cannot view what tasks were linked after I enter them. 
- [ ] For timesheet, I'd like to see all hours accounted for a project this week, but also all hours overall.
- [ ] When editing inputs on task content view and task detail view, the input transitions to a very bright font against a very bright background. Font should be black.
- [ ] Once I've clicked on a task-add input, I can't use the up and down error keys to move to other tasks. Fix.
- [ ] It's also not clear that you can edit Notes in Task Detail View, since they are automatically rendered as markdown. 

## Regression


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
