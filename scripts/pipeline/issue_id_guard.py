#!/usr/bin/env python3
"""Shared issue-id validation helpers for weekly pipeline tooling."""

from __future__ import annotations

import datetime as dt
import re

ISSUE_ID_PATTERN = re.compile(r"(\d{4})-(\d{2})")


def issue_id_max_week(year: int) -> int:
    return dt.date(year, 12, 28).isocalendar().week


def validate_issue_id(issue_id: str | None) -> None:
    if not issue_id:
        return

    m = ISSUE_ID_PATTERN.fullmatch(issue_id)
    if not m:
        raise ValueError(f"Invalid issue id '{issue_id}'. Expected format YYYY-WW.")

    year = int(m.group(1))
    week = int(m.group(2))
    max_week = issue_id_max_week(year)

    if week < 1 or week > max_week:
        raise ValueError(
            f"Invalid issue id '{issue_id}'. Week must be between 01 and {max_week:02d} for {year}."
        )
