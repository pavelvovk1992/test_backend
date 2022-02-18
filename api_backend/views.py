from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api_backend.models import Participant, ParticipantMatch
from api_backend.serializers import ParticipantMatchSerializer, ParticipantCreateSerializer, ParticipantListSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    Класс ViewSet для участников

    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sex", "first_name", "last_name"]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return ParticipantListSerializer
        return super().get_serializer_class()


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
