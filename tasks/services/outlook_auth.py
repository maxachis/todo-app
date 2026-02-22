from __future__ import annotations

import json

import msal
from django.conf import settings

SCOPES = ["Mail.ReadWrite"]


def load_token_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    cache_path = settings.OUTLOOK_TOKEN_CACHE_FILE
    if cache_path.exists():
        cache.deserialize(cache_path.read_text())
    return cache


def save_token_cache(cache: msal.SerializableTokenCache) -> None:
    if cache.has_state_changed:
        settings.OUTLOOK_TOKEN_CACHE_FILE.write_text(cache.serialize())


def get_msal_app(cache: msal.SerializableTokenCache | None = None) -> msal.PublicClientApplication:
    if cache is None:
        cache = load_token_cache()
    authority = f"https://login.microsoftonline.com/{settings.OUTLOOK_TENANT_ID}"
    return msal.PublicClientApplication(
        settings.OUTLOOK_CLIENT_ID,
        authority=authority,
        token_cache=cache,
    )


def acquire_token_silent() -> str | None:
    cache = load_token_cache()
    app = get_msal_app(cache)
    accounts = app.get_accounts()
    if not accounts:
        return None
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    save_token_cache(cache)
    if result and "access_token" in result:
        return result["access_token"]
    return None


def initiate_device_code_flow() -> tuple[msal.PublicClientApplication, dict, msal.SerializableTokenCache]:
    cache = load_token_cache()
    app = get_msal_app(cache)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError(f"Failed to initiate device flow: {json.dumps(flow, indent=2)}")
    return app, flow, cache


def acquire_token_by_device_code(
    app: msal.PublicClientApplication,
    flow: dict,
    cache: msal.SerializableTokenCache,
) -> dict:
    result = app.acquire_token_by_device_flow(flow)
    save_token_cache(cache)
    return result
