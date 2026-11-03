from django.test import TestCase

# Create your tests here.
import pytest
from cards.models import Deck, Card


@pytest.mark.django_db
def test_card_str_includes_reading():
    deck = Deck.objects.create(name="N5 Vocab", level="N5")
    card = Card.objects.create(deck=deck, front="猫", reading="ねこ", meaning="cat")
    assert str(card) == "猫 (ねこ)"