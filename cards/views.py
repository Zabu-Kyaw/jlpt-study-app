from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from .models import Deck


@login_required
def deck_list(request):
    mine = Q(cards__review__user=request.user)
    decks = Deck.objects.annotate(
        card_count=Count("cards", distinct=True),
        studied=Count("cards__review", filter=mine, distinct=True),
        due=Count(
            "cards__review",
            filter=mine & Q(cards__review__due_at__lte=timezone.now()),
            distinct=True,
        ),
    ).order_by("-level", "name")  # N5 first, then N4, N3, N2
    return render(request, "cards/deck_list.html", {"decks": decks})