from datetime import date, datetime
from typing import Optional

from ninja import Schema


class OrgTypeSchema(Schema):
    id: int
    name: str


class OrgTypeCreateInput(Schema):
    name: str


class OrgTypeUpdateInput(Schema):
    name: Optional[str] = None


class InteractionTypeSchema(Schema):
    id: int
    name: str


class InteractionTypeCreateInput(Schema):
    name: str


class InteractionTypeUpdateInput(Schema):
    name: Optional[str] = None


class PersonSchema(Schema):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    notes: str
    follow_up_cadence_days: Optional[int]
    created_at: datetime
    updated_at: datetime


class PersonCreateInput(Schema):
    first_name: str
    middle_name: str = ""
    last_name: str
    notes: str = ""
    follow_up_cadence_days: Optional[int] = None


class PersonUpdateInput(Schema):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    notes: Optional[str] = None
    follow_up_cadence_days: Optional[int] = None


class OrganizationSchema(Schema):
    id: int
    name: str
    org_type_id: int
    notes: str
    created_at: datetime
    updated_at: datetime


class OrganizationCreateInput(Schema):
    name: str
    org_type_id: int
    notes: str = ""


class OrganizationUpdateInput(Schema):
    name: Optional[str] = None
    org_type_id: Optional[int] = None
    notes: Optional[str] = None


class InteractionSchema(Schema):
    id: int
    person_id: int
    interaction_type_id: int
    date: date
    notes: str
    created_at: datetime
    updated_at: datetime


class InteractionCreateInput(Schema):
    person_id: int
    interaction_type_id: int
    date: date
    notes: str = ""


class InteractionUpdateInput(Schema):
    person_id: Optional[int] = None
    interaction_type_id: Optional[int] = None
    date: Optional[date] = None
    notes: Optional[str] = None


class RelationshipPersonPersonSchema(Schema):
    id: int
    person_1_id: int
    person_2_id: int
    notes: str
    created_at: datetime
    updated_at: datetime


class RelationshipPersonPersonCreateInput(Schema):
    person_1_id: int
    person_2_id: int
    notes: str = ""


class RelationshipPersonPersonUpdateInput(Schema):
    notes: Optional[str] = None


class RelationshipOrganizationPersonSchema(Schema):
    id: int
    organization_id: int
    person_id: int
    notes: str
    created_at: datetime
    updated_at: datetime


class RelationshipOrganizationPersonCreateInput(Schema):
    organization_id: int
    person_id: int
    notes: str = ""


class RelationshipOrganizationPersonUpdateInput(Schema):
    notes: Optional[str] = None


class TaskPersonLinkSchema(Schema):
    id: int
    task_id: int
    person_id: int
    created_at: datetime


class TaskOrganizationLinkSchema(Schema):
    id: int
    task_id: int
    organization_id: int
    created_at: datetime


class InteractionTaskLinkSchema(Schema):
    id: int
    interaction_id: int
    task_id: int
    created_at: datetime


class LinkByIdInput(Schema):
    id: int
