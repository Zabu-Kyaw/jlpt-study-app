from django.contrib.auth import get_user_model
from django.urls import reverse

GOOD = {"username": "newuser", "password1": "S7rong-pass-123", "password2": "S7rong-pass-123"}


def test_signup_creates_user_and_logs_in(client, db):
    response = client.post(reverse("signup"), GOOD)
    assert response.status_code == 302
    assert get_user_model().objects.filter(username="newuser").exists()
    assert client.get(reverse("deck_list")).status_code == 200


def test_signup_rejects_mismatched_passwords(client, db):
    response = client.post(reverse("signup"), {**GOOD, "password2": "different-pass-456"})
    assert response.status_code == 200
    assert not get_user_model().objects.filter(username="newuser").exists()