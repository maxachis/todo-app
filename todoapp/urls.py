from django.contrib import admin
from django.urls import path
from django.views.static import serve

import todoapp.settings as settings
from tasks.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path(
        "service-worker.js",
        serve,
        {"document_root": settings.STATICFILES_DIRS[0], "path": "service-worker.js"},
    ),
]
