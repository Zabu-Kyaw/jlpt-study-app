from rest_framework import serializers

from cards.models import Card, Deck


class DeckSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Deck
        fields = ["id", "name", "level", "card_count"]


class AnswerSubmissionSerializer(serializers.Serializer):
    card = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())
    choice = serializers.IntegerField()