from rest_framework import serializers

from django.contrib.auth.models import User
from api_backend.models import Participant, ParticipantMatch


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор Пользователя

    """

    class Meta:
        model = User
        # fields = ["id", "username", "password", "first_name", "last_name", "email"]
        fields = ["id", "username", "password", "email"]


class ParticipantCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации участника

    """

    user = UserSerializer(many=False)

    class Meta:
        model = Participant
        depth = 2
        fields = ["id", "first_name", "last_name", "sex", "avatar", "user"]

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["user"]["email"], username=validated_data["user"]["username"],
            first_name=validated_data["first_name"], last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["user"]["password"])
        user.save()
        try:
            avatar = validated_data["avatar"]
        except:
            avatar = None
        validated_data["email"] = validated_data["user"]["email"]
        validated_data.pop("user")
        Participant.objects.create(
            user=user, **validated_data)
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

    class Meta:
        model = ParticipantMatch
        fields = ["id"]
