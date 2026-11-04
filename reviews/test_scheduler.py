from reviews.scheduler import MIN_EASE, ReviewState, next_state


def test_first_correct_answer_gives_one_day():
    s = next_state(ReviewState(), True)
    assert (s.repetitions, s.interval_days) == (1, 1)


def test_interval_grows_with_consecutive_correct_answers():
    s = ReviewState()
    intervals = []
    for _ in range(4):
        s = next_state(s, True)
        intervals.append(s.interval_days)
    assert intervals == [1, 6, 15, 38]


def test_correct_answers_keep_ease_factor():
    s = next_state(ReviewState(), True)
    assert s.ease_factor == 2.5


def test_wrong_answer_resets_progress_and_lowers_ease():
    s = next_state(ReviewState(ease_factor=2.5, interval_days=15, repetitions=3), False)
    assert (s.repetitions, s.interval_days) == (0, 1)
    assert s.ease_factor == 2.18


def test_ease_never_drops_below_minimum():
    s = ReviewState()
    for _ in range(20):
        s = next_state(s, False)
    assert s.ease_factor == MIN_EASE