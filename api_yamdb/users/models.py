from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLES = [
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор')
]


class CustomUserManager(UserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if username == 'me':
            raise ValueError('"me" is invalid username')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role, **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):

    role = models.CharField(
        choices=ROLES,
        default='user',
        blank=False,
        null=False,
        max_length=10,
        verbose_name='Роль',
    )
    username = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Юзернейм',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    objects = CustomUserManager()

    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == ROLES[2][0]

    @property
    def is_moderator(self):
        return self.role == ROLES[1][0]
