from __future__ import annotations

from datetime import date, datetime, time

from ninja import Schema


class ProjectSchema(Schema):
    id: int
    name: str
    description: str
    is_active: bool
    position: int
    total_hours: float | None = None
    linked_lists_count: int | None = None
    total_tasks: int | None = None
    completed_tasks: int | None = None


class ProjectCreateInput(Schema):
    name: str
    description: str = ""


class ProjectUpdateInput(Schema):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class TagSchema(Schema):
    id: int
    name: str


class TagInput(Schema):
    name: str


class TaskSchema(Schema):
    id: int
    section_id: int
    parent_id: int | None
    title: str
    notes: str
    priority: int
    due_date: date | None
    due_time: time | None
    is_completed: bool
    completed_at: datetime | None
    created_at: datetime
    position: int
    external_id: str | None
    is_pinned: bool
    tags: list[TagSchema] = []
    subtasks: list[TaskSchema] = []
    recurrence_type: str = "none"
    recurrence_rule: dict = {}
    next_occurrence_id: int | None = None


class TaskCreateInput(Schema):
    title: str
    parent_id: int | None = None


class TaskUpdateInput(Schema):
    title: str | None = None
    notes: str | None = None
    due_date: date | None = None
    due_time: time | None = None
    priority: int | None = None
    recurrence_type: str | None = None
    recurrence_rule: dict | None = None


class TaskMoveInput(Schema):
    position: int | None = None
    section_id: int | None = None
    parent_id: int | None = None
    list_id: int | None = None


class SectionSchema(Schema):
    id: int
    list_id: int
    name: str
    emoji: str
    position: int
    tasks: list[TaskSchema] = []


class SectionCreateInput(Schema):
    name: str
    emoji: str = ""


class SectionUpdateInput(Schema):
    name: str | None = None
    emoji: str | None = None


class ListSchema(Schema):
    id: int
    name: str
    emoji: str
    position: int
    project_id: int | None
    sections: list[SectionSchema] = []


class ListCreateInput(Schema):
    name: str
    emoji: str = ""
    project_id: int | None = None


class ListUpdateInput(Schema):
    name: str | None = None
    emoji: str | None = None
    project_id: int | None = None


class MoveInput(Schema):
    position: int


class UpcomingTaskSchema(Schema):
    id: int
    title: str
    due_date: date
    due_time: time | None
    priority: int
    is_pinned: bool
    list_id: int
    list_name: str
    list_emoji: str
    section_id: int
    section_name: str
    tags: list[str] = []


class TimeEntrySchema(Schema):
    id: int
    project_id: int
    task_ids: list[int] = []
    description: str
    date: date
    created_at: datetime


class TimeEntryCreateInput(Schema):
    project_id: int
    date: date
    description: str = ""
    task_ids: list[int] = []
