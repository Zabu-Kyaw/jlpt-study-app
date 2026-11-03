import random

from .models import Card


def pick_next_card(deck):
    return Card.objects.filter(deck=deck).order_by("?").first()


def build_choices(card, num_distractors=3):
    """Return the correct card plus wrong options, shuffled."""
    distractors = list(
        Card.objects.filter(deck=card.deck, kind=card.kind)
        .exclude(pk=card.pk)
        .exclude(meaning=card.meaning)
        .order_by("?")[:num_distractors]
    )
    choices = [card] + distractors
    random.shuffle(choices)
    return choices