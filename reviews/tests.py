import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from cards.models import Card, Deck
from cards.quiz import build_choices
from reviews.models import Answer

from datetime import timedelta

from django.utils import timezone

from reviews.models import Review
from reviews.services import pick_next_card, record_answer

@pytest.fixture
def deck(db):
    deck = Deck.objects.create(name="N5 Vocab", level="N5")
    for front, meaning in [("猫", "cat"), ("犬", "dog"), ("水", "water"), ("本", "book")]:
        Card.objects.create(deck=deck, front=front, meaning=meaning)
    return deck


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("tester", password="pass12345")


def test_build_choices_has_correct_card_and_no_duplicates(deck):
    card = deck.cards.first()
    choices = build_choices(card)
    assert card in choices
    assert len(choices) == 4
    assert len({c.pk for c in choices}) == 4


def test_quiz_requires_login(client, deck):
    response = client.get(reverse("quiz_question", args=[deck.pk]))
    assert response.status_code == 302
    assert "/login/" in response.url


def test_correct_answer_is_recorded(client, user, deck):
    client.force_login(user)
    card = client.get(reverse("quiz_question", args=[deck.pk])).context["card"]
    response = client.post(reverse("quiz_answer", args=[deck.pk]), {"choice": card.pk})
    assert response.context["is_correct"] is True
    assert Answer.objects.filter(user=user, card=card, is_correct=True).count() == 1


def test_wrong_answer_is_recorded(client, user, deck):
    client.force_login(user)
    card = client.get(reverse("quiz_question", args=[deck.pk])).context["card"]
    wrong = Card.objects.exclude(pk=card.pk).first()
    response = client.post(reverse("quiz_answer", args=[deck.pk]), {"choice": wrong.pk})
    assert response.context["is_correct"] is False
    assert Answer.objects.filter(user=user, card=card, is_correct=False).count() == 1

def test_first_answer_creates_review(user, deck):
    card = deck.cards.first()
    _, review = record_answer(user, card, True)
    assert review.interval_days == 1
    assert review.repetitions == 1
    assert review.due_at > timezone.now()


def test_wrong_answer_resets_review(user, deck):
    card = deck.cards.first()
    record_answer(user, card, True)
    _, review = record_answer(user, card, False)
    assert review.repetitions == 0
    assert review.interval_days == 1


def test_pick_prefers_due_cards(user, deck):
    card = deck.cards.first()
    record_answer(user, card, True)
    Review.objects.filter(user=user, card=card).update(
        due_at=timezone.now() - timedelta(minutes=1)
    )
    assert pick_next_card(user, deck) == card


def test_pick_skips_cards_not_yet_due(user, deck):
    card = deck.cards.first()
    record_answer(user, card, True)
    for _ in range(20):
        assert pick_next_card(user, deck) != card


def test_pick_returns_none_when_everything_is_done(user, deck):
    for card in deck.cards.all():
        record_answer(user, card, True)
    assert pick_next_card(user, deck) is None