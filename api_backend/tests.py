from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth.models import User
from api_backend.models import ParticipantMatch, Participant
from api_backend.serializers import ParticipantListSerializer, ParticipantCreateSerializer


class PaticipantTests(APITestCase):

    def setUp(self):
        user_1 = User.objects.create_user(username='UserTest', password='qwerty123')
        user_2 = User.objects.create_user(username='UserTest2', password='qwerty123')
        self.client.force_authenticate(user_1)
        self.participant_1 = Participant.objects.create(user=user_1, first_name="blum", last_name="glor", email="fkuh@rambler.ru", sex="woman")
        Participant.objects.create(user=user_2, first_name="blor", last_name="glum", email="fkuh@rambler.ru", sex=",man")

    def test_participants_list(self):
        response = self.client.get(reverse("clients-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(
            {'id': 1,
             'sex': 'woman',
             'first_name': 'blum',
             'last_name': 'glor',
             'email': 'fkuh@rambler.ru',
             'avatar': 'http://testserver/media/images/avatars/1_default_avatar.jpg',
             'user': 1
             } in response.json()
        )

    def test_participant_detail(self):
        response = self.client.get(reverse("client-detail", kwargs={"pk": self.participant_1.id}))
        serializer_data = ParticipantListSerializer(self.participant_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data["first_name"], response.data["first_name"])
