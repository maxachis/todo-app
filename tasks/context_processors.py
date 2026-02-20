def active_nav(request):
    """Return the active navigation section based on URL path."""
    path = request.path
    if path.startswith("/projects"):
        return {"active_nav": "projects"}
    elif path.startswith("/timesheet"):
        return {"active_nav": "timesheet"}
    elif path.startswith("/import"):
        return {"active_nav": "import"}
    return {"active_nav": "todo"}
