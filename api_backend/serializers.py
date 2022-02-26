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
        fields = ["id", "username", "password"]


class ParticipantCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации участника

    """

    user = UserSerializer(many=False)

    class Meta:
        model = Participant
        fields = ["id", "first_name", "last_name", "email", "sex", "avatar", "user"]

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["user"]["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["user"]["password"])
        user.save()
        validated_data.pop("user")
        try:
            avatar = validated_data["avatar"]
        except:
            avatar = None
        Participant.objects.create(
            user=user, **validated_data)
        validated_data["почта"] = validated_data["email"]
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
    participant = serializers.PrimaryKeyRelatedField(many=True, queryset=Participant.objects.all())
    class Meta:
        model = ParticipantMatch
        fields = ["id", "user", "participant"]
