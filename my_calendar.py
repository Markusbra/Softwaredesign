"""
my_calendar module

This module provides small calendar utilities:
- leap year check (Gregorian rules)
- day of week calculation (algorithm with month codes and century adjustments)
- week number calculation (simple week-of-year estimate)

The functions are implemented without external dependencies.
"""

from __future__ import annotations


def is_leap_year(year: int) -> bool:
    """
    Return True if the given year is a leap year in the Gregorian calendar.

    Rules:
    - divisible by 4 and not divisible by 100, OR divisible by 400

    Args:
        year: Year number (e.g. 2024)

    Returns:
        True if leap year, otherwise False.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def day_of_week(day: int, month: int, year: int) -> str:
    """
    Return the weekday name for a given date using the outlined algorithm
    (month codes, last two digits * 1.25, century adjustments).

    Notes:
    - The algorithm is intended for years >= 1753.
    - The weekday mapping is:
      remainder 1 -> Sunday, 2 -> Monday, ..., 6 -> Friday, 0 -> Saturday

    Args:
        day: Day of month (1..31)
        month: Month (1..12)
        year: Year (>= 1753)

    Returns:
        Weekday as a string, e.g. "Tuesday".

    Raises:
        ValueError: If year < 1753 or invalid month.
    """
    if year < 1753:
        raise ValueError("This algorithm is intended for years >= 1753.")
    if month < 1 or month > 12:
        raise ValueError("Month must be in 1..12.")

    month_code = {
        1: 1,   # Jan
        2: 4,   # Feb
        3: 4,   # Mar
        4: 0,   # Apr
        5: 2,   # May
        6: 5,   # Jun
        7: 0,   # Jul
        8: 3,   # Aug
        9: 6,   # Sep
        10: 1,  # Oct
        11: 4,  # Nov
        12: 6,  # Dec
    }

    weekday = {
        1: "Sunday",
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday",
        0: "Saturday",
    }

    yy = year % 100
    base = int(yy * 1.25) + day + month_code[month]

    # leap year correction for Jan/Feb in this algorithm
    if is_leap_year(year) and month in (1, 2):
        base -= 1

    # century adjustments as described
    if year < 1800:
        base += 4
    elif year < 1900:
        base += 2

    if 2000 < year <= 2100:
        base -= 1

    return weekday[base % 7]


def week_number(day: int, month: int, year: int) -> int:
    """
    Return an approximate week number for the given date using a simple approach:
    compute day-of-year and divide by 7.

    Args:
        day: Day of month (1..31)
        month: Month (1..12)
        year: Year

    Returns:
        Week number as integer (starting at 0 for the first partial week).
    """
    # month lengths (non-leap)
    month_len = {
        1: 31, 2: 28, 3: 31, 4: 30,
        5: 31, 6: 30, 7: 31, 8: 31,
        9: 30, 10: 31, 11: 30, 12: 31
    }

    if is_leap_year(year):
        month_len[2] = 29

    day_of_year = day + sum(month_len[m] for m in range(1, month))
    return day_of_year // 7

def date_summary(day: int, month: int, year: int) -> dict[str, object]:
    """
    Return a dictionary containing:
    - leapyear (bool)
    - weekday (str)
    - week (int)
    """
    return {
        "leapyear": is_leap_year(year),
        "weekday": day_of_week(day, month, year),
        "week": week_number(day, month, year),
    }