from rest_framework import viewsets


from api_backend.serializers import UserSerizalizer, ParticipantMatchSerializer
from django.contrib.auth.models import User
from api_backend.models import Participant, ParticipantMatch


class UserViewSet(viewsets.ModelViewSet):
    """
    Класс ViewSet для пользователей

    """
    queryset = User.objects.all()
    serializer_class = UserSerizalizer


class ParticipantMatchViewSet(viewsets.ModelViewSet):
    """
    Класс ViewSet для оценок участников

    """
    queryset = ParticipantMatch.objects.all()
    serializer_class = ParticipantMatchSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        user = self.request.user
        serializer.save(user=user)
        serializer.save(participant=Participant.objects.get(id=pk))
