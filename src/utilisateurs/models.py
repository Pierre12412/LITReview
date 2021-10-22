from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    photo = models.ImageField(name="photo", upload_to='photos/', null=True, default='user_default.png')