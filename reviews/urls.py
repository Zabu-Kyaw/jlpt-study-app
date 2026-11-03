from django.urls import path

from . import views

urlpatterns = [
    path("<int:deck_id>/", views.quiz_question, name="quiz_question"),
    path("<int:deck_id>/answer/", views.quiz_answer, name="quiz_answer"),
]