from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cards.models import Deck
from cards.quiz import build_choices
from reviews.services import pick_next_card, record_answer
from reviews.stats import get_dashboard_stats

from .serializers import AnswerSubmissionSerializer, DeckSerializer


@api_view(["GET"])
def deck_list(request):
    decks = Deck.objects.annotate(card_count=Count("cards")).order_by("level", "name")
    return Response(DeckSerializer(decks, many=True).data)


@api_view(["GET"])
def next_question(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    card = pick_next_card(request.user, deck)
    if card is None:
        return Response({"done": True, "question": None})
    return Response(
        {
            "done": False,
            "question": {
                "card_id": card.pk,
                "front": card.front,
                "kind": card.kind,
                "choices": [{"id": c.pk, "meaning": c.meaning} for c in build_choices(card)],
            },
        }
    )


@api_view(["POST"])
def submit_answer(request):
    serializer = AnswerSubmissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    card = serializer.validated_data["card"]
    is_correct = serializer.validated_data["choice"] == card.pk
    _, review = record_answer(request.user, card, is_correct)
    return Response(
        {
            "is_correct": is_correct,
            "correct_answer": {
                "id": card.pk,
                "front": card.front,
                "reading": card.reading,
                "meaning": card.meaning,
            },
            "next_review_in_days": review.interval_days,
        }
    )


@api_view(["GET"])
def stats(request):
    return Response(get_dashboard_stats(request.user))