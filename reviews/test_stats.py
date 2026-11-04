from datetime import date, timedelta

from reviews.stats import calculate_streak

TODAY = date(2026, 11, 4)


def days_ago(*offsets):
    return {TODAY - timedelta(days=n) for n in offsets}


def test_no_activity_means_no_streak():
    assert calculate_streak(set(), TODAY) == 0


def test_today_only():
    assert calculate_streak(days_ago(0), TODAY) == 1


def test_streak_survives_until_end_of_today():
    assert calculate_streak(days_ago(1, 2), TODAY) == 2


def test_three_consecutive_days():
    assert calculate_streak(days_ago(0, 1, 2), TODAY) == 3


def test_gap_breaks_streak():
    assert calculate_streak(days_ago(0, 2, 3), TODAY) == 1