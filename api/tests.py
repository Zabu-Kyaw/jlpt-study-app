from django.urls import reverse

from reviews.models import Answer


def test_api_requires_authentication(client, deck):
    response = client.get(reverse("api_deck_list"))
    assert response.status_code == 403


def test_deck_list(api_client, deck):
    response = api_client.get(reverse("api_deck_list"))
    assert response.status_code == 200
    assert response.json()[0]["card_count"] == 4


def test_next_question_returns_four_choices(api_client, deck):
    response = api_client.get(reverse("api_next_question", args=[deck.pk]))
    data = response.json()
    assert data["done"] is False
    assert len(data["question"]["choices"]) == 4


def test_submit_correct_answer(api_client, user, deck):
    card = deck.cards.first()
    response = api_client.post(
        reverse("api_submit_answer"), {"card": card.pk, "choice": card.pk}, format="json"
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert Answer.objects.filter(user=user, card=card, is_correct=True).exists()


def test_submit_answer_rejects_bad_input(api_client, deck):
    response = api_client.post(
        reverse("api_submit_answer"), {"card": 99999, "choice": 1}, format="json"
    )
    assert response.status_code == 400