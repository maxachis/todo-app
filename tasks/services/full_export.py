from __future__ import annotations

import json
from datetime import date, datetime, time

from django.http import HttpResponse
from django.utils import timezone

from network.models import (
    Interaction,
    InteractionTask,
    InteractionType,
    Lead,
    LeadTask,
    Organization,
    OrgType,
    Person,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
    TaskOrganization,
    TaskPerson,
)
from notebook.models import Page, PageLink
from tasks.models import List, Project, ProjectLink, Section, Tag, Task, TimeEntry


def _serialize_value(val):
    """Convert non-JSON-serializable types to strings."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.isoformat()
    if isinstance(val, date):
        return str(val)
    if isinstance(val, time):
        return val.isoformat()
    return val


# ── tasks app serializers ──


def _serialize_tag(tag):
    return {"id": tag.id, "name": tag.name}


def _serialize_project(project):
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "is_active": project.is_active,
        "position": project.position,
    }


def _serialize_project_link(link):
    return {
        "id": link.id,
        "project_id": link.project_id,
        "url": link.url,
        "descriptor": link.descriptor,
        "created_at": _serialize_value(link.created_at),
    }


def _serialize_list(lst):
    return {
        "id": lst.id,
        "name": lst.name,
        "emoji": lst.emoji,
        "position": lst.position,
        "project_id": lst.project_id,
    }


def _serialize_section(section):
    return {
        "id": section.id,
        "list_id": section.list_id,
        "name": section.name,
        "emoji": section.emoji,
        "position": section.position,
    }


def _serialize_task(task):
    return {
        "id": task.id,
        "section_id": task.section_id,
        "parent_id": task.parent_id,
        "title": task.title,
        "notes": task.notes,
        "due_date": _serialize_value(task.due_date),
        "due_time": _serialize_value(task.due_time),
        "is_completed": task.is_completed,
        "completed_at": _serialize_value(task.completed_at),
        "created_at": _serialize_value(task.created_at),
        "position": task.position,
        "external_id": task.external_id,
        "is_pinned": task.is_pinned,
        "recurrence_type": task.recurrence_type,
        "recurrence_rule": task.recurrence_rule,
        "tag_ids": list(task.tags.values_list("id", flat=True)),
    }


def _serialize_time_entry(entry):
    return {
        "id": entry.id,
        "project_id": entry.project_id,
        "description": entry.description,
        "date": _serialize_value(entry.date),
        "created_at": _serialize_value(entry.created_at),
        "task_ids": list(entry.tasks.values_list("id", flat=True)),
    }


# ── network app serializers ──


def _serialize_person(person):
    return {
        "id": person.id,
        "first_name": person.first_name,
        "middle_name": person.middle_name,
        "last_name": person.last_name,
        "email": person.email,
        "linkedin_url": person.linkedin_url,
        "notes": person.notes,
        "follow_up_cadence_days": person.follow_up_cadence_days,
        "created_at": _serialize_value(person.created_at),
        "updated_at": _serialize_value(person.updated_at),
    }


def _serialize_organization(org):
    return {
        "id": org.id,
        "name": org.name,
        "org_type_id": org.org_type_id,
        "notes": org.notes,
        "created_at": _serialize_value(org.created_at),
        "updated_at": _serialize_value(org.updated_at),
    }


def _serialize_org_type(ot):
    return {"id": ot.id, "name": ot.name}


def _serialize_interaction(interaction):
    return {
        "id": interaction.id,
        "person_ids": list(interaction.people.values_list("id", flat=True)),
        "interaction_type_id": interaction.interaction_type_id,
        "date": _serialize_value(interaction.date),
        "notes": interaction.notes,
        "created_at": _serialize_value(interaction.created_at),
        "updated_at": _serialize_value(interaction.updated_at),
    }


def _serialize_interaction_type(it):
    return {"id": it.id, "name": it.name}


def _serialize_lead(lead):
    return {
        "id": lead.id,
        "title": lead.title,
        "status": lead.status,
        "notes": lead.notes,
        "person_id": lead.person_id,
        "organization_id": lead.organization_id,
        "created_at": _serialize_value(lead.created_at),
        "updated_at": _serialize_value(lead.updated_at),
    }


def _serialize_lead_task(lt):
    return {
        "id": lt.id,
        "lead_id": lt.lead_id,
        "task_id": lt.task_id,
        "created_at": _serialize_value(lt.created_at),
    }


def _serialize_relationship_pp(rel):
    return {
        "id": rel.id,
        "person_1_id": rel.person_1_id,
        "person_2_id": rel.person_2_id,
        "notes": rel.notes,
        "created_at": _serialize_value(rel.created_at),
        "updated_at": _serialize_value(rel.updated_at),
    }


def _serialize_relationship_op(rel):
    return {
        "id": rel.id,
        "organization_id": rel.organization_id,
        "person_id": rel.person_id,
        "notes": rel.notes,
        "created_at": _serialize_value(rel.created_at),
        "updated_at": _serialize_value(rel.updated_at),
    }


def _serialize_task_person(tp):
    return {
        "id": tp.id,
        "task_id": tp.task_id,
        "person_id": tp.person_id,
        "created_at": _serialize_value(tp.created_at),
    }


def _serialize_task_organization(to):
    return {
        "id": to.id,
        "task_id": to.task_id,
        "organization_id": to.organization_id,
        "created_at": _serialize_value(to.created_at),
    }


def _serialize_interaction_task(it):
    return {
        "id": it.id,
        "interaction_id": it.interaction_id,
        "task_id": it.task_id,
        "created_at": _serialize_value(it.created_at),
    }


# ── notebook app serializers ──


def _serialize_notebook_page(page):
    return {
        "id": page.id,
        "title": page.title,
        "slug": page.slug,
        "content": page.content,
        "page_type": page.page_type,
        "date": _serialize_value(page.date),
        "created_at": _serialize_value(page.created_at),
        "updated_at": _serialize_value(page.updated_at),
    }


def _serialize_page_link(link):
    return {
        "id": link.id,
        "source_page_id": link.source_page_id,
        "target_page_id": link.target_page_id,
    }


# ── top-level export ──


def export_full_database():
    """Build the complete database export as a dict."""
    return {
        "format": "nexus-full-backup",
        "version": 1,
        "exported_at": timezone.now().isoformat(),
        # tasks app
        "tags": [_serialize_tag(t) for t in Tag.objects.all()],
        "projects": [_serialize_project(p) for p in Project.objects.all()],
        "project_links": [_serialize_project_link(pl) for pl in ProjectLink.objects.all()],
        "lists": [_serialize_list(l) for l in List.objects.all()],
        "sections": [_serialize_section(s) for s in Section.objects.all()],
        "tasks": [_serialize_task(t) for t in Task.objects.all()],
        "time_entries": [_serialize_time_entry(te) for te in TimeEntry.objects.all()],
        # network app
        "org_types": [_serialize_org_type(ot) for ot in OrgType.objects.all()],
        "interaction_types": [
            _serialize_interaction_type(it) for it in InteractionType.objects.all()
        ],
        "people": [_serialize_person(p) for p in Person.objects.all()],
        "organizations": [_serialize_organization(o) for o in Organization.objects.all()],
        "interactions": [_serialize_interaction(i) for i in Interaction.objects.all()],
        "leads": [_serialize_lead(l) for l in Lead.objects.all()],
        "lead_tasks": [_serialize_lead_task(lt) for lt in LeadTask.objects.all()],
        "relationships_person_person": [
            _serialize_relationship_pp(r) for r in RelationshipPersonPerson.objects.all()
        ],
        "relationships_organization_person": [
            _serialize_relationship_op(r)
            for r in RelationshipOrganizationPerson.objects.all()
        ],
        "task_persons": [_serialize_task_person(tp) for tp in TaskPerson.objects.all()],
        "task_organizations": [
            _serialize_task_organization(to) for to in TaskOrganization.objects.all()
        ],
        "interaction_tasks": [
            _serialize_interaction_task(it) for it in InteractionTask.objects.all()
        ],
        # notebook app
        "notebook_pages": [_serialize_notebook_page(p) for p in Page.objects.all()],
        "page_links": [_serialize_page_link(pl) for pl in PageLink.objects.all()],
    }
