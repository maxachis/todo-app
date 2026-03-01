from django.shortcuts import get_object_or_404
from ninja import Router

from notebook.api.schemas import (
    PageBacklink,
    PageCreateInput,
    PageListItem,
    PageMention,
    PageOut,
    PageUpdateInput,
)
from notebook.mentions import reconcile_mentions
from notebook.models import Page, PageEntityMention

router = Router(tags=["notebook"])


def _snippet(content: str, length: int = 150) -> str:
    if len(content) <= length:
        return content
    return content[:length] + "..."


def _serialize_page(page: Page) -> PageOut:
    mentions = [
        PageMention(entity_type=m.entity_type, entity_id=m.entity_id)
        for m in page.entity_mentions.all()
    ]
    backlinks = [
        PageBacklink(
            id=link.source_page.id,
            title=link.source_page.title,
            slug=link.source_page.slug,
            page_type=link.source_page.page_type,
            date=link.source_page.date,
            snippet=_snippet(link.source_page.content),
        )
        for link in page.incoming_links.select_related("source_page").all()
    ]
    return PageOut(
        id=page.id,
        title=page.title,
        slug=page.slug,
        content=page.content,
        page_type=page.page_type,
        date=page.date,
        entity_mentions=mentions,
        backlinks=backlinks,
        created_at=page.created_at,
        updated_at=page.updated_at,
    )


@router.get("/notebook/pages/", response=list[PageListItem])
def list_pages(request, search: str | None = None, page_type: str | None = None):
    qs = Page.objects.order_by("-updated_at")
    if search:
        qs = qs.filter(title__icontains=search)
    if page_type:
        qs = qs.filter(page_type=page_type)
    return [
        PageListItem(
            id=p.id,
            title=p.title,
            slug=p.slug,
            page_type=p.page_type,
            date=p.date,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in qs
    ]


@router.post("/notebook/pages/", response={201: PageOut})
def create_page(request, payload: PageCreateInput):
    if payload.page_type == "daily" and payload.date:
        page, _created = Page.objects.get_or_create(
            page_type="daily",
            date=payload.date,
            defaults={
                "title": str(payload.date),
                "slug": str(payload.date),
                "content": payload.content,
            },
        )
        if not _created and payload.content:
            page.content = payload.content
            page.save()
            reconcile_mentions(page)
        elif _created and page.content:
            reconcile_mentions(page)
        return 201, _serialize_page(page)

    page = Page(
        title=payload.title.strip() or "Untitled",
        content=payload.content,
        page_type=payload.page_type,
        date=payload.date,
    )
    page.save()
    if page.content:
        reconcile_mentions(page)
    return 201, _serialize_page(page)


@router.get("/notebook/pages/{slug}/", response=PageOut)
def get_page(request, slug: str):
    page = get_object_or_404(Page, slug=slug)
    return _serialize_page(page)


@router.put("/notebook/pages/{slug}/", response=PageOut)
def update_page(request, slug: str, payload: PageUpdateInput):
    page = get_object_or_404(Page, slug=slug)
    if payload.title is not None:
        page.title = payload.title.strip() or page.title
    if payload.content is not None:
        page.content = payload.content
    page.save()
    reconcile_mentions(page)
    return _serialize_page(page)


@router.delete("/notebook/pages/{slug}/", response={204: None})
def delete_page(request, slug: str):
    page = get_object_or_404(Page, slug=slug)
    page.delete()
    return 204, None


@router.get(
    "/notebook/mentions/{entity_type}/{entity_id}/",
    response=list[PageBacklink],
)
def entity_mentions(request, entity_type: str, entity_id: int):
    mentions = (
        PageEntityMention.objects.filter(entity_type=entity_type, entity_id=entity_id)
        .select_related("page")
        .order_by("-page__updated_at")
    )
    return [
        PageBacklink(
            id=m.page.id,
            title=m.page.title,
            slug=m.page.slug,
            page_type=m.page.page_type,
            date=m.page.date,
            snippet=_snippet(m.page.content),
        )
        for m in mentions
    ]
