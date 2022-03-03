import os.path
from django.db import models
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from PIL import Image

from api_backend.utils import sending_mail


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

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.avatar:
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

# @receiver(m2m_changed, sender=ParticipantMatch.participant.through)
# def create_matched_message(sender, action, instance, **kwargs):
#     if action == "post_add":
#         for participant in instance.participant.all():
#             print(participant.user)
#             print(ParticipantMatch.objects.get(user=participant.user))
#             #  Объект оценивания оцениваемОГО участника
#             participant_matches = ParticipantMatch.objects.get(user=participant.user)
#             print(participant_matches.participant.filter(participant=instance.participant))





# @receiver(post_save, sender=ParticipantMatch)
# def create_matched_message(sender, instance, created, **kwargs):
#     if created:
#         print(1)

        # #  Пробуем достать объект ParticipantMatch оцениваемого участника по отношению к юзеру.
        # try:
        #     participant_matches = ParticipantMatch.objects.filter(user=participant.user)
        #     # participant_match = ParticipantMatch.objects.filter(user=participant.user)\
        #     #                                         .get(participant=Participant.objects.get(user=user))
        # except:
        #     participant_matches = None
        # print(participant_matches)
        # if participant_match and participant_match.match and instance.match:
        #     sending_mail(
        #         instance.user.username,
        #         participant.user.username,
        #         participant.user.email,
        #         user.email
        #     )


"""
Цветущим вдоль дорог алым розам проще, нежели белым.
Они не меняют цвета.
"""