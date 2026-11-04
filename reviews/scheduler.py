from dataclasses import dataclass

MIN_EASE = 1.3
CORRECT_QUALITY = 4
INCORRECT_QUALITY = 2


@dataclass(frozen=True)
class ReviewState:
    ease_factor: float = 2.5
    interval_days: int = 0
    repetitions: int = 0


def next_state(state: ReviewState, is_correct: bool) -> ReviewState:
    """Return the new review state after an answer (simplified SM-2)."""
    quality = CORRECT_QUALITY if is_correct else INCORRECT_QUALITY

    if quality >= 3:
        if state.repetitions == 0:
            interval = 1
        elif state.repetitions == 1:
            interval = 6
        else:
            interval = max(1, round(state.interval_days * state.ease_factor))
        repetitions = state.repetitions + 1
    else:
        repetitions = 0
        interval = 1

    delta = 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    ease = max(MIN_EASE, round(state.ease_factor + delta, 2))

    return ReviewState(ease_factor=ease, interval_days=interval, repetitions=repetitions)