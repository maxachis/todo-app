"""
Shared fixtures for Playwright E2E tests.

Uses a subprocess Django dev server. Both the test process and the server
share a temporary SQLite database (via the DB_PATH env var) so that
production data is never touched.

Layered seed fixtures:
  seed_list → seed_list_with_tasks → seed_full
Tests pick the minimal data they need.
"""

import os
import socket
import subprocess
import time

import django

# Allow ORM calls from Playwright's async context
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoapp.settings")
django.setup()

import pytest

from tasks.models import List, Section, Tag, Task


def fresh_from_db(model_instance):
    """Re-fetch a model instance with a fresh DB connection.

    Since the server subprocess and test process use separate SQLite
    connections, the test connection may cache stale reads. Closing
    and reopening the connection ensures we see the server's writes.
    """
    from django.db import connection

    connection.close()
    model_instance.refresh_from_db()
    return model_instance


# ─── Override pytest-django to use production DB ───


@pytest.fixture(scope="session")
def django_db_setup():
    """No-op: skip test DB creation. Use production DB so the subprocess
    server shares the same data."""


@pytest.fixture(scope="session")
def django_db_modify_db_settings():
    """No-op: don't modify DB settings."""


# ─── Unblock DB for all e2e tests ─────────────────


@pytest.fixture(autouse=True, scope="session")
def _unblock_db(django_db_blocker):
    """Unblock DB access for all e2e tests at session scope."""
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()


# ─── Live Server (session-scoped subprocess) ───────


def _find_free_port():
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture(scope="session")
def base_url(tmp_path_factory):
    """Create a temp DB, run migrations, start a Django dev server, return its URL."""
    from django.conf import settings
    from django.db import connection

    # 1. Create a temp DB path shared by test process and server subprocess
    db_path = str(tmp_path_factory.mktemp("db") / "test.sqlite3")
    os.environ["DB_PATH"] = db_path

    # 2. Point the test process at the temp DB and reconnect
    settings.DATABASES["default"]["NAME"] = db_path
    connection.close()

    # 3. Run migrations so the temp DB has all tables
    subprocess.run(
        ["python", "manage.py", "migrate", "--run-syncdb"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env=os.environ,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # 4. Start the dev server (inherits DB_PATH from env)
    port = _find_free_port()
    env = os.environ.copy()

    proc = subprocess.Popen(
        ["python", "manage.py", "runserver", f"0.0.0.0:{port}", "--noreload"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    url = f"http://localhost:{port}"

    # Wait for server to be ready
    for _ in range(50):
        try:
            sock = socket.socket()
            sock.connect(("localhost", port))
            sock.close()
            break
        except ConnectionRefusedError:
            time.sleep(0.2)
    else:
        proc.kill()
        raise RuntimeError("Dev server did not start in time")

    yield url

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

    # Clean up env var
    os.environ.pop("DB_PATH", None)


# ─── Page Configuration ────────────────────────────


@pytest.fixture()
def page(page):
    """Configure each Playwright page with reasonable defaults."""
    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(10_000)
    return page


# ─── Database Reset ────────────────────────────────


@pytest.fixture(autouse=True)
def _reset_db():
    """Clear all data before each test."""
    Task.objects.all().delete()
    Section.objects.all().delete()
    List.objects.all().delete()
    Tag.objects.all().delete()


# ─── Seed Fixtures (layered) ──────────────────────


@pytest.fixture()
def seed_list():
    """Create a single list with one section. Returns (list, section)."""
    task_list = List.objects.create(name="Test List", emoji="📋", position=10)
    section = Section.objects.create(list=task_list, name="To Do", position=10)
    return task_list, section


@pytest.fixture()
def seed_list_with_tasks(seed_list):
    """Create a list with 3 tasks in one section.

    Returns (list, section, [task1, task2, task3]).
    """
    task_list, section = seed_list
    tasks = []
    for i, title in enumerate(["Buy groceries", "Walk the dog", "Read a book"], 1):
        tasks.append(
            Task.objects.create(
                section=section, title=title, position=i * 10
            )
        )
    return task_list, section, tasks


@pytest.fixture()
def seed_full(seed_list_with_tasks):
    """Create a fuller dataset: 2 lists, 2 sections, tasks with tags + subtask.

    Returns dict with all objects for flexible access.
    """
    task_list, section1, tasks = seed_list_with_tasks

    section2 = Section.objects.create(
        list=task_list, name="In Progress", position=20
    )
    task_in_progress = Task.objects.create(
        section=section2, title="Write report", position=10
    )

    # Subtask
    subtask = Task.objects.create(
        section=section1,
        parent=tasks[0],
        title="Buy milk",
        position=10,
    )

    # Tags
    tag_urgent = Tag.objects.create(name="urgent")
    tag_home = Tag.objects.create(name="home")
    tasks[0].tags.add(tag_urgent, tag_home)

    # Second list
    list2 = List.objects.create(name="Work", emoji="💼", position=20)
    section_work = Section.objects.create(list=list2, name="Backlog", position=10)
    work_task = Task.objects.create(
        section=section_work, title="Review PRs", position=10
    )

    return {
        "list1": task_list,
        "list2": list2,
        "section1": section1,
        "section2": section2,
        "section_work": section_work,
        "tasks": tasks,
        "subtask": subtask,
        "task_in_progress": task_in_progress,
        "work_task": work_task,
        "tag_urgent": tag_urgent,
        "tag_home": tag_home,
    }
