from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        'user',
        'moderator',
        'admin',
    ]
    
    role = models.TextField(
        ROLES,
        blank = True,
    )
