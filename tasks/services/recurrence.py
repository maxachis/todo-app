from __future__ import annotations

import calendar
import re
from datetime import date, timedelta


class RecurrenceValidationError(Exception):
    pass


def compute_next_due_date(
    recurrence_type: str,
    recurrence_rule: dict,
    current_due_date: date | None,
) -> date:
    today = date.today()
    base = current_due_date or today

    if recurrence_type == "daily":
        next_date = base + timedelta(days=1)
        while next_date <= today:
            next_date += timedelta(days=1)
        return next_date

    if recurrence_type == "weekly":
        days = sorted(recurrence_rule.get("days", []))
        next_date = base + timedelta(days=1)
        for _ in range(8):
            if next_date.weekday() in days and next_date > today:
                return next_date
            next_date += timedelta(days=1)
        # Wrap to next week
        next_date = today + timedelta(days=1)
        for _ in range(7):
            if next_date.weekday() in days:
                return next_date
            next_date += timedelta(days=1)
        return next_date

    if recurrence_type == "monthly":
        day_of_month = recurrence_rule.get("day_of_month", 1)
        year, month = base.year, base.month
        # Move to next month
        month += 1
        if month > 12:
            month = 1
            year += 1
        clamped_day = min(day_of_month, calendar.monthrange(year, month)[1])
        next_date = date(year, month, clamped_day)
        while next_date <= today:
            month += 1
            if month > 12:
                month = 1
                year += 1
            clamped_day = min(day_of_month, calendar.monthrange(year, month)[1])
            next_date = date(year, month, clamped_day)
        return next_date

    if recurrence_type == "yearly":
        target_month = recurrence_rule.get("month", 1)
        target_day = recurrence_rule.get("day", 1)
        year = base.year + 1
        clamped_day = min(target_day, calendar.monthrange(year, target_month)[1])
        next_date = date(year, target_month, clamped_day)
        while next_date <= today:
            year += 1
            clamped_day = min(target_day, calendar.monthrange(year, target_month)[1])
            next_date = date(year, target_month, clamped_day)
        return next_date

    if recurrence_type == "custom_dates":
        dates_strs = recurrence_rule.get("dates", [])
        parsed = []
        for d in dates_strs:
            month_num, day_num = int(d[:2]), int(d[3:5])
            parsed.append((month_num, day_num))

        # Find next date after today
        for year_offset in range(0, 3):
            year = today.year + year_offset
            for month_num, day_num in parsed:
                clamped_day = min(day_num, calendar.monthrange(year, month_num)[1])
                candidate = date(year, month_num, clamped_day)
                if candidate > today:
                    return candidate

        # Fallback: first date next year
        m, d = parsed[0]
        return date(today.year + 1, m, d)

    raise ValueError(f"Unknown recurrence type: {recurrence_type}")


_MM_DD_PATTERN = re.compile(r"^\d{2}-\d{2}$")


def validate_recurrence_rule(recurrence_type: str, recurrence_rule: dict) -> None:
    if recurrence_type == "none":
        return

    if recurrence_type == "daily":
        return

    if recurrence_type == "weekly":
        days = recurrence_rule.get("days")
        if not isinstance(days, list) or len(days) == 0:
            raise RecurrenceValidationError("Weekly recurrence requires a non-empty 'days' list.")
        for d in days:
            if not isinstance(d, int) or d < 0 or d > 6:
                raise RecurrenceValidationError(
                    f"Invalid weekday: {d}. Valid days are 0 (Monday) through 6 (Sunday)."
                )
        return

    if recurrence_type == "monthly":
        day_of_month = recurrence_rule.get("day_of_month")
        if not isinstance(day_of_month, int) or day_of_month < 1 or day_of_month > 31:
            raise RecurrenceValidationError(
                f"Invalid day_of_month: {day_of_month}. Must be between 1 and 31."
            )
        return

    if recurrence_type == "yearly":
        month = recurrence_rule.get("month")
        day = recurrence_rule.get("day")
        if not isinstance(month, int) or month < 1 or month > 12:
            raise RecurrenceValidationError(f"Invalid month: {month}. Must be between 1 and 12.")
        if not isinstance(day, int) or day < 1 or day > 31:
            raise RecurrenceValidationError(f"Invalid day: {day}. Must be between 1 and 31.")
        return

    if recurrence_type == "custom_dates":
        dates = recurrence_rule.get("dates")
        if not isinstance(dates, list) or len(dates) == 0:
            raise RecurrenceValidationError("Custom dates recurrence requires a non-empty 'dates' list.")
        if len(dates) > 52:
            raise RecurrenceValidationError("Custom dates list cannot exceed 52 entries.")
        for d in dates:
            if not isinstance(d, str) or not _MM_DD_PATTERN.match(d):
                raise RecurrenceValidationError(
                    f"Invalid date format: '{d}'. Expected MM-DD format."
                )
            month_num, day_num = int(d[:2]), int(d[3:5])
            if month_num < 1 or month_num > 12:
                raise RecurrenceValidationError(f"Invalid month in date '{d}'.")
            if day_num < 1 or day_num > 31:
                raise RecurrenceValidationError(f"Invalid day in date '{d}'.")
        return

    valid_types = ("none", "daily", "weekly", "monthly", "yearly", "custom_dates")
    raise RecurrenceValidationError(
        f"Invalid recurrence type: '{recurrence_type}'. Must be one of {valid_types}."
    )
