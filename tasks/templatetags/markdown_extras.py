import datetime

import bleach
import markdown as md
from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "i", "li", "ol", "p", "pre", "strong", "ul",
    "br", "hr", "img", "table", "thead", "tbody", "tr", "th", "td",
    "del", "sup", "sub", "span", "div",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title"],
    "abbr": ["title"],
    "acronym": ["title"],
    "*": ["class"],
}


def _add_target_blank(attrs, new=False):
    """Bleach linkify callback to add target=_blank and rel=noopener noreferrer."""
    attrs[(None, "target")] = "_blank"
    attrs[(None, "rel")] = "noopener noreferrer"
    return attrs


@register.filter(name="linkify")
def linkify_text(value):
    """Auto-link URLs in plain text, escaping HTML first."""
    if not value:
        return ""

    escaped = bleach.clean(value, tags=[], attributes={})
    linked = bleach.linkify(escaped, callbacks=[_add_target_blank])
    return mark_safe(linked)


@register.filter(name="render_markdown")
def render_markdown(value):
    """Render Markdown to sanitized HTML with auto-linked URLs."""
    if not value:
        return ""

    html = md.markdown(value, extensions=["extra", "nl2br", "sane_lists"])

    clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

    linked_html = bleach.linkify(clean_html, callbacks=[_add_target_blank])

    return mark_safe(linked_html)


@register.filter(name="due_date_status")
def due_date_status(due_date):
    """Return 'overdue', 'today', or 'upcoming' based on due_date vs today."""
    if not due_date:
        return ""
    today = timezone.localdate()
    if isinstance(due_date, datetime.datetime):
        due_date = due_date.date()
    if due_date < today:
        return "overdue"
    elif due_date == today:
        return "today"
    return "upcoming"
