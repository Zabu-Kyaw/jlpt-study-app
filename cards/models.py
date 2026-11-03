from django.db import models


class Deck(models.Model):
    class Level(models.TextChoices):
        N5 = "N5"
        N4 = "N4"
        N3 = "N3"
        N2 = "N2"
        N1 = "N1"

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=2, choices=Level.choices)

    def __str__(self):
        return f"{self.name} ({self.level})"


class Card(models.Model):
    class Kind(models.TextChoices):
        VOCAB = "vocab"
        GRAMMAR = "grammar"

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards")
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.VOCAB)
    front = models.CharField(max_length=200)
    reading = models.CharField(max_length=200, blank=True)
    meaning = models.CharField(max_length=300)
    example = models.TextField(blank=True)

    def __str__(self):
        return f"{self.front} ({self.reading})" if self.reading else self.front