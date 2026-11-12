from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse

from cards.quiz import build_choices
from reviews.services import record_answer

# Create your tests here.
import pytest
from cards.models import Deck, Card


@pytest.mark.django_db
def test_card_str_includes_reading():
    deck = Deck.objects.create(name="N5 Vocab", level="N5")
    card = Card.objects.create(deck=deck, front="猫", reading="ねこ", meaning="cat")
    assert str(card) == "猫 (ねこ)"

@pytest.mark.django_db
def test_import_cards_is_idempotent(tmp_path):
    csv_file = tmp_path / "cards.csv"
    csv_file.write_text(
        "level,kind,front,reading,meaning,example\n"
        "N5,vocab,猫,ねこ,cat,猫がいます。\n",
        encoding="utf-8",
    )
    call_command("import_cards", str(csv_file))
    call_command("import_cards", str(csv_file))
    assert Card.objects.count() == 1

@pytest.mark.django_db
def test_import_keeps_words_with_different_readings(tmp_path):
    csv_file = tmp_path / "cards.csv"
    csv_file.write_text(
        "level,kind,front,reading,meaning,example\n"
        "N5,vocab,年,とし,year,\n"
        "N5,vocab,年,ねん,year (counter),\n",
        encoding="utf-8",
    )
    call_command("import_cards", str(csv_file))
    assert Card.objects.filter(front="年").count() == 2


@pytest.mark.django_db
def test_build_choices_never_repeats_a_meaning():
    deck = Deck.objects.create(name="N5 Vocab", level="N5")
    target = Card.objects.create(deck=deck, front="猫", meaning="cat")
    for front in ["青", "青い", "蒼"]:
        Card.objects.create(deck=deck, front=front, meaning="blue")
    for front, meaning in [("犬", "dog"), ("水", "water")]:
        Card.objects.create(deck=deck, front=front, meaning=meaning)
    for _ in range(20):
        meanings = [c.meaning for c in build_choices(target)]
        assert len(meanings) == len(set(meanings))


def test_deck_list_shows_progress(client, user, deck):
    record_answer(user, deck.cards.first(), True)
    client.force_login(user)
    response = client.get(reverse("deck_list"))
    first = response.context["decks"][0]
    assert first.card_count == 4
    assert first.studied == 1

@pytest.mark.django_db
def test_theme_toggle_is_on_the_login_page(client):
    response = client.get(reverse("login"))
    assert b'id="theme-toggle"' in response.content