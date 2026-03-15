from datetime import datetime
from typing import Optional

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.errors import HttpError

from network.models import ContactDraft, Organization, OrgType, Person
from notebook.mentions import (
    auto_dismiss_sibling_drafts,
    rewrite_new_contact_mentions,
)

router = Router(tags=["contact-drafts"])


# --- Schemas ---


class ContactDraftSchema(Schema):
    id: int
    name: str
    quick_notes: str
    source_page_id: Optional[int]
    source_page_slug: Optional[str]
    source_page_title: Optional[str]
    dismissed: bool
    created_at: datetime


class ContactDraftMatchesSchema(Schema):
    people: list[dict]
    organizations: list[dict]


class PromoteToPersonInput(Schema):
    first_name: str
    last_name: str
    middle_name: str = ""
    email: str = ""
    linkedin_url: str = ""
    notes: Optional[str] = None
    follow_up_cadence_days: Optional[int] = None


class PromoteToOrgInput(Schema):
    name: str
    org_type_id: int
    notes: Optional[str] = None


class LinkInput(Schema):
    person_id: Optional[int] = None
    org_id: Optional[int] = None


# --- Helpers ---


def _serialize_draft(draft: ContactDraft) -> ContactDraftSchema:
    return ContactDraftSchema(
        id=draft.id,
        name=draft.name,
        quick_notes=draft.quick_notes,
        source_page_id=draft.source_page_id,
        source_page_slug=draft.source_page.slug if draft.source_page else None,
        source_page_title=draft.source_page.title if draft.source_page else None,
        dismissed=draft.dismissed,
        created_at=draft.created_at,
    )


def _append_notes(record, quick_notes):
    """Append quick_notes to an existing record's notes field."""
    if not quick_notes:
        return
    if record.notes:
        record.notes = f"{record.notes}\n---\n{quick_notes}"
    else:
        record.notes = quick_notes
    record.save(update_fields=["notes"])


# --- Endpoints ---


@router.get("/contact-drafts/", response=list[ContactDraftSchema])
def list_drafts(request):
    drafts = (
        ContactDraft.objects.filter(
            promoted_to_person__isnull=True,
            promoted_to_org__isnull=True,
            dismissed=False,
        )
        .select_related("source_page")
        .order_by("-created_at")
    )
    return [_serialize_draft(d) for d in drafts]


@router.get("/contact-drafts/{draft_id}/", response=ContactDraftSchema)
def get_draft(request, draft_id: int):
    draft = get_object_or_404(
        ContactDraft.objects.select_related("source_page"), pk=draft_id
    )
    return _serialize_draft(draft)


@router.delete("/contact-drafts/{draft_id}/", response={204: None})
def delete_draft(request, draft_id: int):
    draft = get_object_or_404(ContactDraft, pk=draft_id)
    draft.delete()
    return 204, None


@router.post("/contact-drafts/{draft_id}/dismiss/", response=ContactDraftSchema)
def dismiss_draft(request, draft_id: int):
    draft = get_object_or_404(
        ContactDraft.objects.select_related("source_page"), pk=draft_id
    )
    draft.dismissed = True
    draft.save(update_fields=["dismissed"])
    return _serialize_draft(draft)


@router.post("/contact-drafts/{draft_id}/promote/person/", response={201: dict})
def promote_to_person(request, draft_id: int, payload: PromoteToPersonInput):
    draft = get_object_or_404(ContactDraft, pk=draft_id)

    first_name = payload.first_name.strip()
    last_name = payload.last_name.strip()
    if not first_name:
        raise HttpError(422, "First name may not be blank.")
    if not last_name:
        raise HttpError(422, "Last name may not be blank.")

    if Person.objects.filter(
        first_name__iexact=first_name, last_name__iexact=last_name
    ).exists():
        raise HttpError(
            409, f"A person named {first_name} {last_name} already exists."
        )

    notes = payload.notes if payload.notes is not None else draft.quick_notes

    person = Person.objects.create(
        first_name=first_name,
        middle_name=payload.middle_name.strip(),
        last_name=last_name,
        email=payload.email.strip(),
        linkedin_url=payload.linkedin_url.strip(),
        notes=notes,
        follow_up_cadence_days=payload.follow_up_cadence_days,
    )

    draft.promoted_to_person = person
    draft.save(update_fields=["promoted_to_person"])

    rewrite_new_contact_mentions(draft.name, "person", person.id)
    auto_dismiss_sibling_drafts(draft.name, draft.id)

    return 201, {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
    }


@router.post("/contact-drafts/{draft_id}/promote/org/", response={201: dict})
def promote_to_org(request, draft_id: int, payload: PromoteToOrgInput):
    draft = get_object_or_404(ContactDraft, pk=draft_id)

    name = payload.name.strip()
    if not name:
        raise HttpError(422, "Name may not be blank.")

    if Organization.objects.filter(name__iexact=name).exists():
        raise HttpError(409, f"An organization named {name} already exists.")

    org_type = get_object_or_404(OrgType, pk=payload.org_type_id)
    notes = payload.notes if payload.notes is not None else draft.quick_notes

    org = Organization.objects.create(
        name=name,
        org_type=org_type,
        notes=notes,
    )

    draft.promoted_to_org = org
    draft.save(update_fields=["promoted_to_org"])

    rewrite_new_contact_mentions(draft.name, "org", org.id)
    auto_dismiss_sibling_drafts(draft.name, draft.id)

    return 201, {"id": org.id, "name": org.name}


@router.post("/contact-drafts/{draft_id}/link/", response=ContactDraftSchema)
def link_to_existing(request, draft_id: int, payload: LinkInput):
    draft = get_object_or_404(
        ContactDraft.objects.select_related("source_page"), pk=draft_id
    )

    if payload.person_id is not None:
        person = get_object_or_404(Person, pk=payload.person_id)
        _append_notes(person, draft.quick_notes)
        draft.promoted_to_person = person
        draft.save(update_fields=["promoted_to_person"])
        rewrite_new_contact_mentions(draft.name, "person", person.id)
    elif payload.org_id is not None:
        org = get_object_or_404(Organization, pk=payload.org_id)
        _append_notes(org, draft.quick_notes)
        draft.promoted_to_org = org
        draft.save(update_fields=["promoted_to_org"])
        rewrite_new_contact_mentions(draft.name, "org", org.id)
    else:
        raise HttpError(422, "Must provide person_id or org_id.")

    auto_dismiss_sibling_drafts(draft.name, draft.id)
    return _serialize_draft(draft)


@router.get("/contact-drafts/{draft_id}/matches/", response=ContactDraftMatchesSchema)
def get_matches(request, draft_id: int):
    draft = get_object_or_404(ContactDraft, pk=draft_id)

    tokens = draft.name.split()
    people_matches = []
    org_matches = []

    if tokens:
        # People: first token → first_name, last token → last_name
        first_token = tokens[0]
        last_token = tokens[-1] if len(tokens) > 1 else tokens[0]

        people_q = Q(first_name__icontains=first_token) | Q(
            last_name__icontains=last_token
        )
        for p in Person.objects.filter(people_q).distinct()[:10]:
            people_matches.append(
                {"id": p.id, "first_name": p.first_name, "last_name": p.last_name}
            )

    # Organizations: full name containment
    for o in Organization.objects.filter(name__icontains=draft.name)[:10]:
        org_matches.append({"id": o.id, "name": o.name})

    return ContactDraftMatchesSchema(
        people=people_matches, organizations=org_matches
    )
