from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLES = [
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор')
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
