from ninja import NinjaAPI

from network.api import (
    graph,
    interaction_mediums,
    interaction_types,
    interactions,
    leads,
    org_types,
    organizations,
    people,
    person_tags,
    relationships,
    relationship_types,
    task_links,
)
from notebook.api import pages as notebook_pages
from tasks.api import dashboard, export, import_tasks, lists, project_links, projects, search, sections, tags, tasks, timesheet, upcoming

api = NinjaAPI(urls_namespace="tasks_api")
api.add_router("", lists.router)
api.add_router("", sections.router)
api.add_router("", tasks.router)
api.add_router("", tags.router)
api.add_router("", search.router)
api.add_router("", export.router)
api.add_router("", import_tasks.router)
api.add_router("", projects.router)
api.add_router("", project_links.router)
api.add_router("", timesheet.router)
api.add_router("", upcoming.router)
api.add_router("", dashboard.router)
api.add_router("", people.router)
api.add_router("", person_tags.router)
api.add_router("", organizations.router)
api.add_router("", org_types.router)
api.add_router("", interaction_types.router)
api.add_router("", interaction_mediums.router)
api.add_router("", interactions.router)
api.add_router("", relationships.router)
api.add_router("", relationship_types.router)
api.add_router("", task_links.router)
api.add_router("", graph.router)
api.add_router("", leads.router)
api.add_router("", notebook_pages.router)


@api.get("/health/")
def health(request):
    return {"status": "ok"}


@api.post("/csrf-check/")
def csrf_check(request):
    return {"ok": True}
