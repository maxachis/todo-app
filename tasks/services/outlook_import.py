from __future__ import annotations

import html2text

from tasks.models import Section, Task

BODY_MAX_LENGTH = 10_000
TRUNCATION_INDICATOR = "\n\n[... truncated]"


def parse_graph_message(message: dict) -> dict:
    subject = message.get("subject", "(no subject)")

    sender_data = message.get("sender", {}).get("emailAddress", {})
    sender_name = sender_data.get("name", "")
    sender_email = sender_data.get("address", "")
    if sender_name and sender_email:
        sender = f"{sender_name} <{sender_email}>"
    else:
        sender = sender_name or sender_email or ""

    body_obj = message.get("body", {})
    body_content = body_obj.get("content", "")
    body_type = body_obj.get("contentType", "text")

    if body_type.lower() == "html" and body_content:
        converter = html2text.HTML2Text()
        converter.body_width = 0
        converter.ignore_images = True
        body_text = converter.handle(body_content).strip()
    else:
        body_text = body_content.strip()

    if len(body_text) > BODY_MAX_LENGTH:
        body_text = body_text[:BODY_MAX_LENGTH] + TRUNCATION_INDICATOR

    if sender:
        notes = f"From: {sender}\n\n{body_text}"
    else:
        notes = body_text

    return {
        "subject": subject,
        "sender": sender,
        "internet_message_id": message.get("internetMessageId", ""),
        "notes": notes,
        "graph_id": message.get("id", ""),
        "categories": message.get("categories", []),
    }


def create_task_from_email(parsed: dict, section: Section) -> Task | None:
    external_id = parsed["internet_message_id"]
    if not external_id:
        return None

    if Task.objects.filter(external_id=external_id).exists():
        return None

    max_pos = (
        Task.objects.filter(section=section, parent__isnull=True)
        .order_by("-position")
        .values_list("position", flat=True)
        .first()
    ) or 0

    task = Task.objects.create(
        title=parsed["subject"],
        notes=parsed["notes"],
        external_id=external_id,
        section=section,
        position=max_pos + 1,
    )
    return task
