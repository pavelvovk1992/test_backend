from rest_framework import viewsets

from api_backend.serializers import UserSerizalizer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    Класс ViewSet для ползователей
    """

    queryset = User.objects.all()
    serializer_class = UserSerizalizer
