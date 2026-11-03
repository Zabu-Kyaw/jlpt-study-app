import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from cards.models import Card, Deck
from cards.quiz import build_choices
from reviews.models import Answer


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