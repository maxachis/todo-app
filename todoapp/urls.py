from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

import todoapp.settings as settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "service-worker.js",
        serve,
        {"document_root": settings.STATICFILES_DIRS[0], "path": "service-worker.js"},
    ),
    path("", include("tasks.urls")),
]
