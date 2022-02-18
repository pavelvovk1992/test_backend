from rest_framework import serializers

from django.contrib.auth.models import User
from api_backend.models import Participant, ParticipantMatch


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор Пользователя

    """

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]


class ParticipantCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации участника

    """

    user = UserSerializer(many=False)

    class Meta:
        model = Participant
        fields = ["id", "sex", "avatar", "user"]

    def create(self, validated_data):
        sex = validated_data["sex"]
        avatar = validated_data["avatar"]
        email = validated_data["user"]["email"]
        first_name = validated_data["user"]["first_name"]
        last_name = validated_data["user"]["last_name"]
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        Participant.objects.create(user=user, first_name=first_name, last_name=last_name,
                                   email=email, sex=sex, avatar=avatar)
        return Participant(**validated_data)


class ParticipantListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка участников

    """
    class Meta:
        model = Participant
        fields = ["id", "sex", "first_name", "last_name", "email", "avatar", "user"]


class ParticipantMatchSerializer(serializers.ModelSerializer):
    """
    Сериализатор для оценки участника участника

    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    participant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ParticipantMatch
        fields = ["id", "user", "participant", "match"]
