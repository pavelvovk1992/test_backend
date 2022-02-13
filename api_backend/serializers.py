from rest_framework import serializers

from django.contrib.auth.models import User
from api_backend.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    """
    Сериализатор участника.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Participant
        fields = ["id", "sex", "avatar", "user"]


class UserSerizalizer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """

    participant = ParticipantSerializer(many=False)

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email", "participant"]

    def create(self, validated_data):
        participant_data = validated_data.pop("participant")
        user = User.objects.create(**validated_data)
        Participant.objects.create(user=user, **participant_data)
        return user
