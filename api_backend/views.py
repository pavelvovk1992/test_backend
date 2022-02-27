from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
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

    def get_permissions(self):
        if self.action in ["list"]:
            self.permission_classes = [permissions.IsAuthenticated]
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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        participant = Participant.objects.get(id=self.kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.check_user_match(user):
            serializer.save(user=user)
            serializer.save(participant=Participant.objects.filter(id=self.kwargs['pk']))
            return Response({"It's success!": participant.user.email}, status=status.HTTP_201_CREATED)
        else:
            if not self.check_user_matches_participant(user, participant):
                ParticipantMatch.objects.get(user=user).participant.add(self.kwargs['pk'])
                return Response({"It's success!": participant.user.email}, status=status.HTTP_201_CREATED)
            return Response({"Failed": "You have already matched this participant"}, status=status.HTTP_400_BAD_REQUEST)


    def check_user_matches_participant(self, user, participant):
        try:
            existing_match = self.check_user_match(user).get(participant=participant)
        except:
            existing_match = None
        return existing_match

    def check_user_match(self, user):
        try:
            participant_match = ParticipantMatch.objects.filter(user=user)
        except:
            participant_match = None
        return participant_match
