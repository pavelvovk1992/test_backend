import os
import os.path

from django.db import models
from django.contrib.auth.models import User

from PIL import Image

class Participant(models.Model):
    """Модель участника сервиса знакомств"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    first_name = models.CharField("Имя", max_length=20, default="Anon")
    last_name = models.CharField("Фамилия", max_length=25, default="Anonov")
    email = models.CharField(max_length=30, null=True)
    sex = models.CharField("Пол", max_length=15)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="images/default_avatar.jpg"
    )
    longitude = models.FloatField("Долгота", null=True)
    latitude = models.FloatField("Широта", null=True)
    distance = models.FloatField("Расстояние", blank=True, null=True)

    __current_avatar = None

    def __str__(self):
        return self.user.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__current_avatar = self.avatar

    def save(self, *args, **kwargs):
        if self.avatar != self.__current_avatar:
            self.avatar = self.add_watermark()
        super().save(*args, **kwargs)

    def add_watermark(self):
        image_name = os.path.basename(self.avatar.path)
        watermark = Image.open("media/images/watermark.jpg")
        open_image = Image.open(self.avatar)
        open_image.paste(watermark, (50, 50))
        open_image.save(f"media/images/avatars/{self.user_id}_{image_name}")
        watermarked_image = f"images/avatars/{self.user_id}_{image_name}"
        return watermarked_image


class ParticipantMatch(models.Model):
    """Модель оценивания участников"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    participant = models.ManyToManyField(
        Participant,
        verbose_name="Участник",
    )
