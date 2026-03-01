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


class InteractionMediumSchema(Schema):
    id: int
    name: str


class InteractionMediumCreateInput(Schema):
    name: str


class InteractionMediumUpdateInput(Schema):
    name: Optional[str] = None


class InteractionTypeSchema(Schema):
    id: int
    name: str


class InteractionTypeCreateInput(Schema):
    name: str


class InteractionTypeUpdateInput(Schema):
    name: Optional[str] = None


class PersonPersonRelationshipTypeSchema(Schema):
    id: int
    name: str


class PersonPersonRelationshipTypeCreateInput(Schema):
    name: str


class PersonPersonRelationshipTypeUpdateInput(Schema):
    name: Optional[str] = None


class OrgPersonRelationshipTypeSchema(Schema):
    id: int
    name: str


class OrgPersonRelationshipTypeCreateInput(Schema):
    name: str


class OrgPersonRelationshipTypeUpdateInput(Schema):
    name: Optional[str] = None


class PersonTagSchema(Schema):
    id: int
    name: str


class PersonTagInput(Schema):
    name: str


class PersonSchema(Schema):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    email: str
    linkedin_url: str
    notes: str
    follow_up_cadence_days: Optional[int]
    tags: list[PersonTagSchema]
    last_interaction_date: Optional[date]
    last_interaction_type: Optional[str]
    created_at: datetime
    updated_at: datetime


class PersonCreateInput(Schema):
    first_name: str
    middle_name: str = ""
    last_name: str
    email: str = ""
    linkedin_url: str = ""
    notes: str = ""
    follow_up_cadence_days: Optional[int] = None


class PersonUpdateInput(Schema):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
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
    person_ids: list[int]
    organization_ids: list[int] = []
    interaction_type_id: int
    interaction_medium_id: Optional[int] = None
    date: date
    notes: str
    created_at: datetime
    updated_at: datetime


class InteractionCreateInput(Schema):
    person_ids: list[int]
    organization_ids: list[int] = []
    interaction_type_id: int
    interaction_medium_id: Optional[int] = None
    date: date
    notes: str = ""


class InteractionUpdateInput(Schema):
    person_ids: Optional[list[int]] = None
    organization_ids: Optional[list[int]] = None
    interaction_type_id: Optional[int] = None
    interaction_medium_id: Optional[int] = None
    date: Optional[date] = None
    notes: Optional[str] = None


class RelationshipPersonPersonSchema(Schema):
    id: int
    person_1_id: int
    person_2_id: int
    relationship_type_id: Optional[int] = None
    relationship_type_name: Optional[str] = None
    notes: str
    created_at: datetime
    updated_at: datetime


class RelationshipPersonPersonCreateInput(Schema):
    person_1_id: int
    person_2_id: int
    relationship_type_id: Optional[int] = None
    notes: str = ""


class RelationshipPersonPersonUpdateInput(Schema):
    relationship_type_id: Optional[int] = None
    notes: Optional[str] = None


class RelationshipOrganizationPersonSchema(Schema):
    id: int
    organization_id: int
    person_id: int
    relationship_type_id: Optional[int] = None
    relationship_type_name: Optional[str] = None
    notes: str
    created_at: datetime
    updated_at: datetime


class RelationshipOrganizationPersonCreateInput(Schema):
    organization_id: int
    person_id: int
    relationship_type_id: Optional[int] = None
    notes: str = ""


class RelationshipOrganizationPersonUpdateInput(Schema):
    relationship_type_id: Optional[int] = None
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


class LeadSchema(Schema):
    id: int
    title: str
    status: str
    notes: str
    person_id: Optional[int]
    organization_id: Optional[int]
    person_name: Optional[str]
    organization_name: Optional[str]
    created_at: datetime
    updated_at: datetime


class LeadCreateInput(Schema):
    title: str
    status: str = "prospect"
    notes: str = ""
    person_id: Optional[int] = None
    organization_id: Optional[int] = None


class LeadUpdateInput(Schema):
    title: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    person_id: Optional[int] = None
    organization_id: Optional[int] = None


class LeadTaskLinkSchema(Schema):
    id: int
    lead_id: int
    task_id: int
    created_at: datetime


class LinkByIdInput(Schema):
    id: int
