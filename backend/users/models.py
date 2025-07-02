from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_client_user = models.BooleanField(default=False)
    is_ops_user = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
