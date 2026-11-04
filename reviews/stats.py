from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import Answer, Review


def calculate_streak(active_days, today):
    """Count consecutive study days ending today (or yesterday, so the streak survives until midnight)."""
    day = today if today in active_days else today - timedelta(days=1)
    streak = 0
    while day in active_days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def get_dashboard_stats(user):
    answers = Answer.objects.filter(user=user)
    totals = answers.aggregate(
        total=Count("id"), correct=Count("id", filter=Q(is_correct=True))
    )
    total, correct = totals["total"], totals["correct"]

    # TruncDate uses the current timezone (Asia/Tokyo), so "a day" means a Tokyo day
    active_days = set(
        answers.annotate(day=TruncDate("answered_at"))
        .values_list("day", flat=True)
        .distinct()
    )

    weak_rows = (
        answers.values("card_id", "card__front", "card__reading", "card__meaning")
        .annotate(total=Count("id"), wrong=Count("id", filter=Q(is_correct=False)))
        .filter(wrong__gt=0)
        .order_by("-wrong", "-total")[:5]
    )
    weak_cards = [
        {
            "front": row["card__front"],
            "reading": row["card__reading"],
            "meaning": row["card__meaning"],
            "wrong": row["wrong"],
            "total": row["total"],
            "accuracy": round((row["total"] - row["wrong"]) / row["total"] * 100),
        }
        for row in weak_rows
    ]

    return {
        "total": total,
        "correct": correct,
        "accuracy": round(correct / total * 100) if total else None,
        "streak": calculate_streak(active_days, timezone.localdate()),
        "due_now": Review.objects.filter(user=user, due_at__lte=timezone.now()).count(),
        "cards_studied": Review.objects.filter(user=user).count(),
        "weak_cards": weak_cards,
    }