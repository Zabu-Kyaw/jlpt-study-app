from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from cards.models import Card

from .models import Answer, Review
from .scheduler import ReviewState, next_state


@transaction.atomic
def record_answer(user, card, is_correct):
    """Save the answer and update the card's review schedule."""
    now = timezone.now()
    answer = Answer.objects.create(user=user, card=card, is_correct=is_correct)

    review, _ = Review.objects.get_or_create(user=user, card=card)
    new = next_state(
        ReviewState(review.ease_factor, review.interval_days, review.repetitions),
        is_correct,
    )
    review.ease_factor = new.ease_factor
    review.interval_days = new.interval_days
    review.repetitions = new.repetitions
    review.last_reviewed_at = now
    review.due_at = now + timedelta(days=new.interval_days)
    review.save()
    return answer, review


def pick_next_card(user, deck):
    """Due reviews first (oldest due first), then brand-new cards."""
    due = (
        Review.objects.filter(user=user, card__deck=deck, due_at__lte=timezone.now())
        .select_related("card")
        .order_by("due_at")
        .first()
    )
    if due:
        return due.card

    return (
        Card.objects.filter(deck=deck)
        .exclude(review__user=user)
        .order_by("?")
        .first()
    )