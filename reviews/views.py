from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cards.models import Card, Deck
from cards.quiz import build_choices, pick_next_card

from .models import Answer

SESSION_KEY = "quiz_card_id"


@login_required
def quiz_question(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    card = pick_next_card(deck)
    context = {"deck": deck, "card": card}
    if card:
        request.session[SESSION_KEY] = card.pk
        context["choices"] = build_choices(card)
    return render(request, "reviews/quiz_question.html", context)


@login_required
@require_POST
def quiz_answer(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    card_id = request.session.pop(SESSION_KEY, None)
    if card_id is None:
        return redirect("quiz_question", deck_id=deck.pk)

    card = get_object_or_404(Card, pk=card_id, deck=deck)
    try:
        chosen_id = int(request.POST.get("choice", ""))
    except ValueError:
        return redirect("quiz_question", deck_id=deck.pk)

    is_correct = chosen_id == card.pk
    Answer.objects.create(user=request.user, card=card, is_correct=is_correct)
    return render(
        request,
        "reviews/quiz_result.html",
        {
            "deck": deck,
            "card": card,
            "is_correct": is_correct,
            "chosen": Card.objects.filter(pk=chosen_id).first(),
        },
    )