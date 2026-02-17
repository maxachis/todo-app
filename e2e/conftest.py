"""Shared fixtures for Playwright E2E tests against Svelte + Django API."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import django
import pytest

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoapp.settings")
django.setup()

from tasks.models import List, Section, Tag, Task


def fresh_from_db(model_instance):
    from django.db import connection

    connection.close()
    model_instance.refresh_from_db()
    return model_instance


@pytest.fixture(scope="session")
def django_db_setup():
    """Use a shared temp DB instead of pytest-django's test DB."""


@pytest.fixture(scope="session")
def django_db_modify_db_settings():
    """Keep Django DB settings untouched by pytest-django."""


@pytest.fixture(autouse=True, scope="session")
def _unblock_db(django_db_blocker):
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()


def _find_free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_port(port: int, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.25):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError(f"Server on port {port} did not start in time")


@pytest.fixture(scope="session")
def base_url(tmp_path_factory):
    from django.conf import settings
    from django.db import connection

    root = Path(__file__).resolve().parents[1]
    frontend_dir = root / "frontend"

    db_path = str(tmp_path_factory.mktemp("db") / "e2e.sqlite3")
    os.environ["DB_PATH"] = db_path
    settings.DATABASES["default"]["NAME"] = db_path
    connection.close()

    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--run-syncdb"],
        cwd=root,
        env=os.environ.copy(),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    django_port = _find_free_port()
    django_proc = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", f"127.0.0.1:{django_port}", "--noreload"],
        cwd=root,
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    frontend_env = os.environ.copy()
    frontend_env["VITE_API_PROXY_TARGET"] = f"http://127.0.0.1:{django_port}"

    subprocess.run(
        ["npm", "run", "build"],
        cwd=frontend_dir,
        env=frontend_env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    preview_port = _find_free_port()
    preview_proc = subprocess.Popen(
        ["npm", "run", "preview", "--", "--host", "127.0.0.1", "--port", str(preview_port), "--strictPort"],
        cwd=frontend_dir,
        env=frontend_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        _wait_for_port(django_port)
        _wait_for_port(preview_port)
        yield f"http://127.0.0.1:{preview_port}"
    finally:
        for proc in (preview_proc, django_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        os.environ.pop("DB_PATH", None)


@pytest.fixture()
def page(page):
    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(10_000)
    return page


@pytest.fixture(autouse=True)
def _reset_db(base_url):
    Task.objects.all().delete()
    Section.objects.all().delete()
    List.objects.all().delete()
    Tag.objects.all().delete()


@pytest.fixture()
def seed_list(base_url):
    task_list = List.objects.create(name="Test List", emoji="??", position=10)
    section = Section.objects.create(list=task_list, name="To Do", position=10)
    return task_list, section


@pytest.fixture()
def seed_list_with_tasks(seed_list):
    task_list, section = seed_list
    tasks = [
        Task.objects.create(section=section, title="Buy groceries", position=10),
        Task.objects.create(section=section, title="Walk the dog", position=20),
        Task.objects.create(section=section, title="Read a book", position=30),
    ]
    return task_list, section, tasks


@pytest.fixture()
def seed_full(seed_list_with_tasks):
    task_list, section1, tasks = seed_list_with_tasks

    section2 = Section.objects.create(list=task_list, name="In Progress", position=20)
    task_in_progress = Task.objects.create(section=section2, title="Write report", position=10)

    subtask = Task.objects.create(section=section1, parent=tasks[0], title="Buy milk", position=10)

    tag_urgent = Tag.objects.create(name="urgent")
    tag_home = Tag.objects.create(name="home")
    tasks[0].tags.add(tag_urgent, tag_home)

    list2 = List.objects.create(name="Work", emoji="??", position=20)
    section_work = Section.objects.create(list=list2, name="Backlog", position=10)
    work_task = Task.objects.create(section=section_work, title="Review PRs", position=10)

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
