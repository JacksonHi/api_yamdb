from django.db import models
from django.contrib.auth.models import AbstractUser

ROL_USER = 'user'
ROL_MODERATOR = 'moderator'
ROL_ADMIN = 'admin'

ROLES = [
    (ROL_USER, 'Пользователь'),
    (ROL_MODERATOR, 'Модератор'),
    (ROL_ADMIN, 'Администратор')
]


class User(AbstractUser):

    role = models.CharField(
        choices=ROLES,
        blank=False,
        null=False,
        max_length=10
    )
    # role = models.TextField(
    #     ROLES,
    #     blank = True,
    # )
