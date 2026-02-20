"""E2E tests for timesheet presentation."""

import re
from datetime import date

from playwright.sync_api import expect

from tasks.models import Project, TimeEntry


class TestTimesheet:
    def test_entry_shows_local_time_in_record_view(self, page, base_url):
        project = Project.objects.create(name="Timesheet Proj", description="", position=10)
        TimeEntry.objects.create(project=project, date=date.today(), description="Local time test")

        page.goto(f"{base_url}/timesheet")
        expect(page.locator(".entry-row")).to_have_count(1)

        time_text = page.locator(".entry-row .entry-time").first.inner_text().strip()
        assert ":" in time_text
        assert re.search(r"\d", time_text)
