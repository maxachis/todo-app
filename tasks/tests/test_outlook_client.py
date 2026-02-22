from __future__ import annotations

from unittest.mock import MagicMock, patch

from django.test import TestCase


class TestFetchEmailsByCategory(TestCase):
    @patch("tasks.services.outlook_client.requests.get")
    def test_fetches_emails_with_category(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "value": [
                {"id": "msg1", "subject": "Test email"},
                {"id": "msg2", "subject": "Another email"},
            ]
        }
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        from tasks.services.outlook_client import fetch_emails_by_category

        messages = fetch_emails_by_category("fake-token", "ToDo")
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["subject"], "Test email")

        # Verify the URL includes the category filter
        call_url = mock_get.call_args[0][0]
        self.assertIn("categories/any(c:c eq 'ToDo')", call_url)

    @patch("tasks.services.outlook_client.requests.get")
    def test_handles_pagination(self, mock_get):
        page1_resp = MagicMock()
        page1_resp.json.return_value = {
            "value": [{"id": "msg1"}],
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/next-page",
        }
        page1_resp.raise_for_status = MagicMock()

        page2_resp = MagicMock()
        page2_resp.json.return_value = {
            "value": [{"id": "msg2"}],
        }
        page2_resp.raise_for_status = MagicMock()

        mock_get.side_effect = [page1_resp, page2_resp]

        from tasks.services.outlook_client import fetch_emails_by_category

        messages = fetch_emails_by_category("fake-token", "ToDo")
        self.assertEqual(len(messages), 2)
        self.assertEqual(mock_get.call_count, 2)

    @patch("tasks.services.outlook_client.requests.get")
    def test_empty_response(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"value": []}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        from tasks.services.outlook_client import fetch_emails_by_category

        messages = fetch_emails_by_category("fake-token", "ToDo")
        self.assertEqual(messages, [])


class TestUpdateEmailCategories(TestCase):
    @patch("tasks.services.outlook_client.requests.patch")
    def test_updates_categories(self, mock_patch):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_patch.return_value = mock_resp

        from tasks.services.outlook_client import update_email_categories

        update_email_categories("fake-token", "msg-123", ["ToDo-Imported"])

        mock_patch.assert_called_once()
        call_kwargs = mock_patch.call_args
        self.assertIn("msg-123", call_kwargs[0][0])
        self.assertEqual(call_kwargs[1]["json"], {"categories": ["ToDo-Imported"]})
