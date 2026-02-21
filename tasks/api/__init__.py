from ninja import NinjaAPI

from tasks.api import export, import_tasks, lists, projects, search, sections, tags, tasks, timesheet, upcoming

api = NinjaAPI(urls_namespace="tasks_api")
api.add_router("", lists.router)
api.add_router("", sections.router)
api.add_router("", tasks.router)
api.add_router("", tags.router)
api.add_router("", search.router)
api.add_router("", export.router)
api.add_router("", import_tasks.router)
api.add_router("", projects.router)
api.add_router("", timesheet.router)
api.add_router("", upcoming.router)


@api.get("/health/")
def health(request):
    return {"status": "ok"}


@api.post("/csrf-check/")
def csrf_check(request):
    return {"ok": True}
