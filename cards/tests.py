from django.test import TestCase
from django.core.management import call_command

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