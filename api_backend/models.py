import os.path
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from PIL import Image

from api_backend.utils import sending_mail


class Participant(models.Model):
    """Модель участника сервиса знакомств"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=20, default="Anon")
    last_name = models.CharField(max_length=25, default="Anonov")
    email = models.CharField(max_length=30, null=True)
    sex = models.CharField("Пол", max_length=15)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="images/default_avatar.jpg"
    )

    def save(self, *args, **kwargs):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Участник"
    )
    match = models.BooleanField("Совпадение", null=True)

    def save(self, *args, **kwargs):
        if not self.check_existing_match():
            super().save(*args, **kwargs)

    def check_existing_match(self):
        user = self.user
        participant = self.participant

        #  Пробуем достать объект ParticipantMatch юзера по отношению к оцениваемому участнику.
        try:
            participant_match = ParticipantMatch.objects.filter(user=user).get(participant=participant)
        except:
            participant_match = None
        return participant_match


@receiver(post_save, sender=ParticipantMatch)
def create_matched_message(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        participant = instance.participant

        #  Пробуем достать объект ParticipantMatch оцениваемого участника по отношению к юзеру.
        try:
            participant_match = ParticipantMatch.objects.filter(user=participant.user)\
                                                    .get(participant=Participant.objects.get(user=user))
        except:
            participant_match = None
        if participant_match and participant_match.match and instance.match:
            sending_mail(
                instance.user.username,
                participant.user.username,
                participant.user.email,
                user.email
            )
