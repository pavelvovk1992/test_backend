from django.db import IntegrityError

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api_backend.filters import DistanceFilter
from api_backend.models import Participant, ParticipantMatch
from api_backend.serializers import ParticipantMatchSerializer, ParticipantListSerializer, ParticipantCreateSerializer
from api_backend.utils import sending_mail


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    Класс ViewSet для участников

    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = DistanceFilter

    def get_permissions(self):
        if self.action in ["list"]:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

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
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        participant = Participant.objects.filter(id=self.kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=user)
            serializer.save(participant=participant)
            self.mail(user, participant[0], participant[0].user.email, user.email)
            return Response({"It's success!": participant[0].user.email}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            if participant[0] not in ParticipantMatch.objects.get(user=user).participant.all():
                ParticipantMatch.objects.get(user=user).participant.add(self.kwargs['pk'])
                self.mail(user, participant[0], participant[0].user.email, user.email)
                return Response({"It's success!": participant[0].user.email}, status=status.HTTP_201_CREATED)
        return Response({"Failed": "You have already matched this participant"}, status=status.HTTP_400_BAD_REQUEST)

    def mail(self, user, participant, participant_email, user_email):
        try:
            participant_matches = ParticipantMatch.objects.get(user=participant.user)
        except:
            participant_matches = None
        if participant_matches:
            if user.participant in participant_matches.participant.all():
                sending_mail(user, participant, participant_email, user_email)
