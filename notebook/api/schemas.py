import datetime as _dt
from typing import Optional

from ninja import Schema


class PageBacklink(Schema):
    id: int
    title: str
    slug: str
    page_type: str
    date: Optional[_dt.date]
    snippet: str


class PageMention(Schema):
    entity_type: str
    entity_id: int


class PageOut(Schema):
    id: int
    title: str
    slug: str
    content: str
    page_type: str
    date: Optional[_dt.date]
    entity_mentions: list[PageMention]
    backlinks: list[PageBacklink]
    created_at: _dt.datetime
    updated_at: _dt.datetime


class PageListItem(Schema):
    id: int
    title: str
    slug: str
    page_type: str
    date: Optional[_dt.date]
    created_at: _dt.datetime
    updated_at: _dt.datetime


class PageCreateInput(Schema):
    title: str = "Untitled"
    content: str = ""
    page_type: str = "wiki"
    date: Optional[_dt.date] = None


class PageUpdateInput(Schema):
    title: Optional[str] = None
    content: Optional[str] = None
