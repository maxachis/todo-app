from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings


class TestTokenCacheLoadSave(TestCase):
    def test_load_token_cache_no_file(self):
        with override_settings(OUTLOOK_TOKEN_CACHE_FILE=Path("/tmp/nonexistent_cache.json")):
            from tasks.services.outlook_auth import load_token_cache

            cache = load_token_cache()
            # Should return an empty cache without error
            self.assertFalse(cache.has_state_changed)

    def test_load_and_save_token_cache(self, tmp_path=None):
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            cache_path = Path(f.name)
            f.write("{}")

        try:
            with override_settings(OUTLOOK_TOKEN_CACHE_FILE=cache_path):
                from tasks.services.outlook_auth import load_token_cache, save_token_cache

                cache = load_token_cache()
                # Simulate state change
                cache._cache = {"dummy": "data"}
                cache.has_state_changed = True
                save_token_cache(cache)

                # Verify file was written
                content = json.loads(cache_path.read_text())
                self.assertIn("dummy", content)
        finally:
            cache_path.unlink(missing_ok=True)


class TestAcquireTokenSilent(TestCase):
    @patch("tasks.services.outlook_auth.get_msal_app")
    @patch("tasks.services.outlook_auth.load_token_cache")
    @patch("tasks.services.outlook_auth.save_token_cache")
    def test_returns_token_when_available(self, mock_save, mock_load, mock_app):
        mock_cache = MagicMock()
        mock_load.return_value = mock_cache

        mock_msal = MagicMock()
        mock_msal.get_accounts.return_value = [{"username": "user@outlook.com"}]
        mock_msal.acquire_token_silent.return_value = {"access_token": "test-token-123"}
        mock_app.return_value = mock_msal

        from tasks.services.outlook_auth import acquire_token_silent

        token = acquire_token_silent()
        self.assertEqual(token, "test-token-123")
        mock_save.assert_called_once_with(mock_cache)

    @patch("tasks.services.outlook_auth.get_msal_app")
    @patch("tasks.services.outlook_auth.load_token_cache")
    @patch("tasks.services.outlook_auth.save_token_cache")
    def test_returns_none_when_no_accounts(self, mock_save, mock_load, mock_app):
        mock_cache = MagicMock()
        mock_load.return_value = mock_cache

        mock_msal = MagicMock()
        mock_msal.get_accounts.return_value = []
        mock_app.return_value = mock_msal

        from tasks.services.outlook_auth import acquire_token_silent

        token = acquire_token_silent()
        self.assertIsNone(token)

    @patch("tasks.services.outlook_auth.get_msal_app")
    @patch("tasks.services.outlook_auth.load_token_cache")
    @patch("tasks.services.outlook_auth.save_token_cache")
    def test_returns_none_when_silent_fails(self, mock_save, mock_load, mock_app):
        mock_cache = MagicMock()
        mock_load.return_value = mock_cache

        mock_msal = MagicMock()
        mock_msal.get_accounts.return_value = [{"username": "user@outlook.com"}]
        mock_msal.acquire_token_silent.return_value = {"error": "interaction_required"}
        mock_app.return_value = mock_msal

        from tasks.services.outlook_auth import acquire_token_silent

        token = acquire_token_silent()
        self.assertIsNone(token)
