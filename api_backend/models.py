from django.db import models
from django.contrib.auth.models import User


class Participant(models.Model):
    """Модель участника сервиса знакомств"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    sex = models.CharField("Пол", max_length=15)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="images/avatars/default-avatar.jpg"
    )

    def __str__(self):
        return f'{self.user}'
