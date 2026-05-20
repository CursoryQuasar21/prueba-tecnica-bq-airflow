"""Custom Airflow operator for UTC date difference calculations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from airflow.models import BaseOperator


class TimeDiffOperator(BaseOperator):
    """Calculate and log the difference between now in UTC and a date.

    The operator is intentionally small and dependency-free so it can be reused
    in DAG exercises without coupling it to any source system or warehouse.
    """

    template_fields: tuple[str, ...] = ("diff_date",)

    def __init__(self, diff_date: datetime | str, **kwargs: Any) -> None:
        """Create the operator.

        Args:
            diff_date: Reference date used to calculate the difference from the
                current UTC datetime. Naive datetimes are treated as UTC.
            **kwargs: Standard Airflow ``BaseOperator`` keyword arguments.
        """
        super().__init__(**kwargs)
        self.diff_date = diff_date

    def execute(self, context: dict[str, Any]) -> dict[str, float | str | int]:
        """Calculate and log the date difference.

        Args:
            context: Airflow execution context.

        Returns:
            A dictionary with the reference date, current date, difference in
            days, and total difference in seconds.
        """
        parsed_diff_date = self._parse_datetime(self.diff_date)
        current_date = datetime.now(timezone.utc)
        diff = current_date - parsed_diff_date

        result = {
            "diff_date": parsed_diff_date.isoformat(),
            "current_date": current_date.isoformat(),
            "diff_days": diff.days,
            "diff_total_seconds": diff.total_seconds(),
        }

        self.log.info("diff_date: %s", result["diff_date"])
        self.log.info("current_date: %s", result["current_date"])
        self.log.info("difference_days: %s", result["diff_days"])
        self.log.info("difference_total_seconds: %s", result["diff_total_seconds"])

        return result

    @staticmethod
    def _parse_datetime(value: datetime | str) -> datetime:
        """Parse a datetime value and return it as timezone-aware UTC."""
        if isinstance(value, datetime):
            parsed_value = value
        else:
            parsed_value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        if parsed_value.tzinfo is None:
            return parsed_value.replace(tzinfo=timezone.utc)

        return parsed_value.astimezone(timezone.utc)
