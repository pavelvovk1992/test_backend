import django_filters
from geopy.distance import geodesic

from api_backend.models import Participant


class DistanceFilter(django_filters.FilterSet):
    distance = django_filters.CharFilter(
        lookup_expr="до Вас, км.",
        method="filter_participants_by_distance"
    )

    def check_distance(self):
        user = self.request.user
        user_latitude = user.participant.latitude
        user_longitude = user.participant.longitude
        participant_distance = {}
        for participant in Participant.objects.all():
            distance = geodesic((user_latitude, user_longitude), (participant.latitude, participant.longitude)).km
            participant_distance.update({participant: distance})
        return participant_distance

    def filter_participants_by_distance(self, queryset, field_name, value):
        participants = []
        for participant, distance in self.check_distance().items():
            if distance < int(value):
                participants.append(participant.user)
        return Participant.objects.filter(user__in=participants)

    class Meta:
        model = Participant
        fields = ["first_name", "last_name", "sex", "distance"]
