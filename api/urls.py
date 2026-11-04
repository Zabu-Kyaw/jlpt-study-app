from django.urls import path

from . import views

urlpatterns = [
    path("decks/", views.deck_list, name="api_deck_list"),
    path("decks/<int:deck_id>/next/", views.next_question, name="api_next_question"),
    path("answers/", views.submit_answer, name="api_submit_answer"),
    path("stats/", views.stats, name="api_stats"),
]