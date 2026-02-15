from django.urls import path

from tasks.views import export, import_tasks, lists, projects, search, sections, tags, tasks, timesheet

urlpatterns = [
    # Main page
    path("", lists.index, name="index"),
    # Lists
    path("lists/", lists.create_list, name="create_list"),
    path("lists/<int:list_id>/", lists.list_detail, name="list_detail"),
    path("lists/<int:list_id>/update/", lists.update_list, name="update_list"),
    path("lists/<int:list_id>/delete/", lists.delete_list, name="delete_list"),
    path("lists/<int:list_id>/move/", lists.move_list, name="move_list"),
    # Sections
    path(
        "lists/<int:list_id>/sections/",
        sections.create_section,
        name="create_section",
    ),
    path(
        "sections/<int:section_id>/update/",
        sections.update_section,
        name="update_section",
    ),
    path(
        "sections/<int:section_id>/delete/",
        sections.delete_section,
        name="delete_section",
    ),
    path(
        "sections/<int:section_id>/move/",
        sections.move_section,
        name="move_section",
    ),
    # Tasks
    path(
        "sections/<int:section_id>/tasks/",
        tasks.create_task,
        name="create_task",
    ),
    path("tasks/<int:task_id>/detail/", tasks.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/update/", tasks.update_task, name="update_task"),
    path("tasks/<int:task_id>/delete/", tasks.delete_task, name="delete_task"),
    # Task actions
    path(
        "tasks/<int:task_id>/complete/",
        tasks.complete_task,
        name="complete_task",
    ),
    path(
        "tasks/<int:task_id>/uncomplete/",
        tasks.uncomplete_task,
        name="uncomplete_task",
    ),
    path("tasks/<int:task_id>/move/", tasks.move_task, name="move_task"),
    # Tags
    path("tasks/<int:task_id>/tags/", tags.add_tag, name="add_tag"),
    path(
        "tasks/<int:task_id>/tags/<int:tag_id>/",
        tags.remove_tag,
        name="remove_tag",
    ),
    # Export
    path(
        "lists/<int:list_id>/export/<str:fmt>/",
        export.export_list_view,
        name="export_list",
    ),
    path("export/<str:fmt>/", export.export_all_view, name="export_all"),
    # Search
    path("search/", search.search_tasks, name="search_tasks"),
    # Import
    path("import/", import_tasks.import_page, name="import_page"),
    # Projects
    path("projects/", projects.projects_index, name="projects_index"),
    path("projects/create/", projects.create_project, name="create_project"),
    path(
        "projects/<int:project_id>/update/",
        projects.update_project,
        name="update_project",
    ),
    path(
        "projects/<int:project_id>/delete/",
        projects.delete_project,
        name="delete_project",
    ),
    path(
        "projects/<int:project_id>/toggle/",
        projects.toggle_project_active,
        name="toggle_project_active",
    ),
    # Timesheet
    path("timesheet/", timesheet.timesheet_index, name="timesheet_index"),
    path("timesheet/add/", timesheet.create_time_entry, name="create_time_entry"),
    path(
        "timesheet/<int:entry_id>/delete/",
        timesheet.delete_time_entry,
        name="delete_time_entry",
    ),
    path(
        "timesheet/tasks-for-project/<int:project_id>/",
        timesheet.tasks_for_project,
        name="tasks_for_project",
    ),
]
