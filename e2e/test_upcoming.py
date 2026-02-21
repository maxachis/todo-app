"""E2E tests for the upcoming tasks dashboard."""

from datetime import date, timedelta

from playwright.sync_api import expect

from tasks.models import List, Section, Task


class TestUpcomingDashboard:
    def test_dashboard_page_loads(self, page, base_url, seed_list):
        task_list, section = seed_list
        Task.objects.create(
            section=section, title="Due soon", position=10,
            due_date=date.today() + timedelta(days=1),
        )

        page.goto(f"{base_url}/upcoming")

        expect(page.locator("h1")).to_have_text("Upcoming")
        expect(page.locator(".task-row")).to_have_count(1)
        expect(page.locator(".task-title").first).to_have_text("Due soon")

    def test_tasks_grouped_by_time_horizon(self, page, base_url, seed_list):
        task_list, section = seed_list
        today = date.today()
        Task.objects.create(
            section=section, title="Overdue task", position=10,
            due_date=today - timedelta(days=1),
        )
        Task.objects.create(
            section=section, title="Today task", position=20,
            due_date=today,
        )
        Task.objects.create(
            section=section, title="Later task", position=30,
            due_date=today + timedelta(days=14),
        )

        page.goto(f"{base_url}/upcoming")

        expect(page.locator(".task-group")).to_have_count(3)
        groups = page.locator("h2")
        expect(groups.nth(0)).to_contain_text("Overdue")
        expect(groups.nth(1)).to_contain_text("Today")
        expect(groups.nth(2)).to_contain_text("Later")

    def test_clicking_task_navigates_to_list(self, page, base_url, seed_list):
        task_list, section = seed_list
        task = Task.objects.create(
            section=section, title="Navigate me", position=10,
            due_date=date.today(),
        )

        page.goto(f"{base_url}/upcoming")
        page.locator(".task-row").first.click()

        page.wait_for_url(f"**/?list={task_list.id}&task={task.id}")
        expect(page.locator(f'.task-row[data-task-id="{task.id}"]')).to_be_visible()

    def test_empty_state_when_no_upcoming_tasks(self, page, base_url, seed_list):
        page.goto(f"{base_url}/upcoming")

        expect(page.locator(".empty-state")).to_be_visible()
        expect(page.locator(".empty-state p")).to_contain_text("No tasks with due dates")

    def test_shows_list_and_section_context(self, page, base_url):
        task_list = List.objects.create(name="Work", emoji="", position=10)
        section = Section.objects.create(list=task_list, name="Sprint", position=10)
        Task.objects.create(
            section=section, title="Context task", position=10,
            due_date=date.today(),
        )

        page.goto(f"{base_url}/upcoming")

        location = page.locator(".task-location").first
        expect(location).to_contain_text("Work")
        expect(location).to_contain_text("Sprint")
