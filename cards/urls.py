from django.urls import path

from . import views

urlpatterns = [
    path("", views.deck_list, name="deck_list"),
]