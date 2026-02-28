from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import PersonTagInput, PersonTagSchema
from network.models import Person, PersonTag

router = Router(tags=["person-tags"])


@router.get("/person-tags/", response=list[PersonTagSchema])
def list_person_tags(request, exclude_person: int | None = None):
    tags = PersonTag.objects.all()
    if exclude_person is not None:
        person = get_object_or_404(Person, pk=exclude_person)
        tags = tags.exclude(pk__in=person.tags.values_list("id", flat=True))
    return [PersonTagSchema(id=t.id, name=t.name) for t in tags.order_by("name")]


@router.post("/people/{person_id}/tags/", response=list[PersonTagSchema])
def add_person_tag(request, person_id: int, payload: PersonTagInput):
    person = get_object_or_404(Person, pk=person_id)
    name = payload.name.strip()
    if not name:
        raise HttpError(400, "Tag name may not be blank.")

    tag, _ = PersonTag.objects.get_or_create(name=name)
    person.tags.add(tag)
    return [PersonTagSchema(id=t.id, name=t.name) for t in person.tags.order_by("name")]


@router.delete("/people/{person_id}/tags/{tag_id}/", response={204: None})
def remove_person_tag(request, person_id: int, tag_id: int):
    person = get_object_or_404(Person, pk=person_id)
    tag = get_object_or_404(PersonTag, pk=tag_id)
    person.tags.remove(tag)
    return 204, None
