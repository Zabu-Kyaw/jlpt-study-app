import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from cards.models import Card, Deck


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("tester", password="pass12345")


@pytest.fixture
def deck(db):
    deck = Deck.objects.create(name="N5 Vocab", level="N5")
    for front, meaning in [("猫", "cat"), ("犬", "dog"), ("水", "water"), ("本", "book")]:
        Card.objects.create(deck=deck, front=front, meaning=meaning)
    return deck


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client