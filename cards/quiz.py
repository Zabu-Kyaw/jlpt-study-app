import random

from .models import Card


def build_choices(card, num_distractors=3):
    """Return the correct card plus wrong options with distinct meanings, shuffled."""
    candidates = (
        Card.objects.filter(deck=card.deck, kind=card.kind)
        .exclude(meaning=card.meaning)
        .order_by("?")[: num_distractors * 10]
    )
    seen = {card.meaning}
    distractors = []
    for c in candidates:
        if c.meaning not in seen:
            seen.add(c.meaning)
            distractors.append(c)
        if len(distractors) == num_distractors:
            break

    choices = [card] + distractors
    random.shuffle(choices)
    return choices
