from datetime import date
from unittest.mock import patch

from django.test import TestCase

from tasks.services.recurrence import (
    RecurrenceValidationError,
    compute_next_due_date,
    validate_recurrence_rule,
)


class ComputeNextDueDateTests(TestCase):
    @patch("tasks.services.recurrence.date")
    def test_daily(self, mock_date):
        mock_date.today.return_value = date(2026, 2, 20)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("daily", {}, date(2026, 2, 20))
        self.assertEqual(result, date(2026, 2, 21))

    @patch("tasks.services.recurrence.date")
    def test_daily_late_completion(self, mock_date):
        mock_date.today.return_value = date(2026, 2, 25)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("daily", {}, date(2026, 2, 20))
        self.assertEqual(result, date(2026, 2, 26))

    @patch("tasks.services.recurrence.date")
    def test_weekly_next_matching_day(self, mock_date):
        mock_date.today.return_value = date(2026, 2, 20)  # Friday
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("weekly", {"days": [0, 4]}, date(2026, 2, 20))
        # Next Monday is Feb 23
        self.assertEqual(result, date(2026, 2, 23))

    @patch("tasks.services.recurrence.date")
    def test_monthly(self, mock_date):
        mock_date.today.return_value = date(2026, 2, 15)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("monthly", {"day_of_month": 15}, date(2026, 2, 15))
        self.assertEqual(result, date(2026, 3, 15))

    @patch("tasks.services.recurrence.date")
    def test_monthly_clamp_day_31_in_february(self, mock_date):
        mock_date.today.return_value = date(2026, 1, 31)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("monthly", {"day_of_month": 31}, date(2026, 1, 31))
        self.assertEqual(result, date(2026, 2, 28))

    @patch("tasks.services.recurrence.date")
    def test_monthly_late_completion(self, mock_date):
        mock_date.today.return_value = date(2026, 3, 20)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("monthly", {"day_of_month": 15}, date(2026, 2, 15))
        self.assertEqual(result, date(2026, 4, 15))

    @patch("tasks.services.recurrence.date")
    def test_yearly(self, mock_date):
        mock_date.today.return_value = date(2026, 3, 15)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        result = compute_next_due_date("yearly", {"month": 3, "day": 15}, date(2026, 3, 15))
        self.assertEqual(result, date(2027, 3, 15))

    @patch("tasks.services.recurrence.date")
    def test_custom_dates_next_in_list(self, mock_date):
        mock_date.today.return_value = date(2026, 3, 20)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        rule = {"dates": ["03-15", "06-15", "09-15", "12-15"]}
        result = compute_next_due_date("custom_dates", rule, date(2026, 3, 15))
        self.assertEqual(result, date(2026, 6, 15))

    @patch("tasks.services.recurrence.date")
    def test_custom_dates_wraps_to_next_year(self, mock_date):
        mock_date.today.return_value = date(2026, 7, 1)
        mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
        rule = {"dates": ["03-15", "06-15"]}
        result = compute_next_due_date("custom_dates", rule, date(2026, 6, 15))
        self.assertEqual(result, date(2027, 3, 15))


class ValidateRecurrenceRuleTests(TestCase):
    def test_none_always_valid(self):
        validate_recurrence_rule("none", {})

    def test_daily_always_valid(self):
        validate_recurrence_rule("daily", {})

    def test_weekly_valid(self):
        validate_recurrence_rule("weekly", {"days": [0, 2, 4]})

    def test_weekly_empty_days_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("weekly", {"days": []})

    def test_weekly_invalid_day_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("weekly", {"days": [7]})

    def test_monthly_valid(self):
        validate_recurrence_rule("monthly", {"day_of_month": 15})

    def test_monthly_day_32_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("monthly", {"day_of_month": 32})

    def test_monthly_day_0_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("monthly", {"day_of_month": 0})

    def test_yearly_valid(self):
        validate_recurrence_rule("yearly", {"month": 3, "day": 15})

    def test_yearly_invalid_month_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("yearly", {"month": 13, "day": 1})

    def test_custom_dates_valid(self):
        validate_recurrence_rule("custom_dates", {"dates": ["03-15", "06-15"]})

    def test_custom_dates_wrong_format_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("custom_dates", {"dates": ["2026-03-15"]})

    def test_custom_dates_empty_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("custom_dates", {"dates": []})

    def test_custom_dates_over_52_rejected(self):
        dates = [f"{(i % 12) + 1:02d}-{(i % 28) + 1:02d}" for i in range(53)]
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("custom_dates", {"dates": dates})

    def test_invalid_type_rejected(self):
        with self.assertRaises(RecurrenceValidationError):
            validate_recurrence_rule("biweekly", {})
