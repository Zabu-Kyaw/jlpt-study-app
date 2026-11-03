from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from .models import Deck


@login_required
def deck_list(request):
    decks = Deck.objects.annotate(card_count=Count("cards")).order_by("level", "name")
    return render(request, "cards/deck_list.html", {"decks": decks})