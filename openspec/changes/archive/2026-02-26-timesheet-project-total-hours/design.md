## Context

The timesheet page shows a weekly view of time entries with a summary bar displaying total hours and per-project hours for that week. The projects API already computes `total_hours` (all-time count of time entries) via annotation, but this data isn't available on the timesheet page. Users want to see cumulative project effort alongside the weekly snapshot.

Current summary response shape:
```json
{
  "total_hours": 5,
  "per_project": [
    { "project_id": 1, "project_name": "Foo", "hours": 3 }
  ]
}
```

## Goals / Non-Goals

**Goals:**
- Add all-time hours per project and an overall total to the timesheet API summary
- Display these alongside weekly hours in the summary bar with minimal UI overhead

**Non-Goals:**
- Custom date-range queries or arbitrary period summaries
- Changing the projects page or its `total_hours` annotation
- Modifying time entry creation/deletion behavior

## Decisions

### 1. Compute overall hours in the timesheet endpoint (not reuse projects API)

Add a separate aggregation query in `get_timesheet` that counts all `TimeEntry` rows grouped by project. This avoids coupling the timesheet to the projects API and keeps the response self-contained.

**Alternative considered**: Fetch from the projects endpoint or share the annotation logic. Rejected because it would add a dependency between endpoints and return more data than needed (project descriptions, links, etc.).

### 2. Add fields to existing summary shape (not a new top-level key)

Extend the existing `summary` object:
- `summary.overall_total_hours`: integer count of all time entries across all time
- `summary.per_project[].overall_hours`: integer count of all-time entries for each project that appears in the weekly data, plus any projects with all-time hours but zero hours this week

This keeps the response backward-compatible — existing consumers can ignore the new fields.

**Alternative considered**: A separate `overall_summary` object. Rejected because it would duplicate the `per_project` structure and complicate frontend consumption.

### 3. Include projects with zero weekly hours but nonzero overall hours

The `per_project` array should include projects that have all-time entries but none in the current week, so the user sees the full picture of project investment. These appear with `hours: 0` and their `overall_hours` value.

### 4. Display format: "ProjectName: 3h (42h total)"

Show weekly hours first (primary), with overall hours in parentheses as secondary context. The overall total appears similarly: "Total: 5h (120h total)".

## Risks / Trade-offs

- **Additional DB query**: One extra aggregation query per page load. Mitigated by the fact that `TimeEntry` is a small table (single-user app) and the query is a simple `COUNT` with `GROUP BY`. No index changes needed.
- **Wider per_project array**: Including zero-weekly-hours projects could make the summary bar longer if many inactive projects have logged time. Acceptable for a single-user app; can be revisited if it becomes cluttered.
