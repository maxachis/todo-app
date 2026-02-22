from __future__ import annotations

import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def fetch_emails_by_category(access_token: str, category: str) -> list[dict]:
    url = (
        f"{GRAPH_BASE}/me/messages"
        f"?$filter=categories/any(c:c eq '{category}')"
        f"&$select=id,subject,body,sender,internetMessageId,categories"
        f"&$top=50"
    )
    messages = []
    while url:
        resp = requests.get(url, headers=_headers(access_token), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        messages.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return messages


def update_email_categories(
    access_token: str, message_id: str, categories: list[str]
) -> None:
    url = f"{GRAPH_BASE}/me/messages/{message_id}"
    resp = requests.patch(
        url,
        headers=_headers(access_token),
        json={"categories": categories},
        timeout=30,
    )
    resp.raise_for_status()
