import os.path
from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Participant(models.Model):
    """Модель участника сервиса знакомств"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    sex = models.CharField("Пол", max_length=15)
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="images/default_avatar.jpg"
    )

    def add_watermark(self):
        image_name = os.path.basename(self.avatar.path)
        watermark = Image.open("media/images/watermark.jpg")
        open_image = Image.open(self.avatar)
        open_image.paste(watermark, (50, 50))
        open_image.save(f"media/images/avatars/{self.user_id}_{image_name}")
        watermarked_image = f"images/avatars/{self.user_id}_{image_name}"
        return watermarked_image

    def save(self, *args, **kwargs):
        self.avatar = self.add_watermark()
        super().save(*args, **kwargs)
