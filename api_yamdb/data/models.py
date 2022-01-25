from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, UserManager
from pytils.translit import slugify


ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLES = [
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор')
]


class CustomUserManager(UserManager):
    
    def create_user(self, username, email, password,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        if username == 'me':
            raise ValueError('"me" is invalid username')
        return super().create_user(username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email, password, role, **extra_fields):
        return super().create_superuser(username, email, password, role='admin', **extra_fields)


class User(AbstractUser):

    role = models.CharField(
        choices=ROLES,
        default='user',
        blank=False,
        null=False,
        max_length=10
    )
    username = models.CharField(
        max_length=200,
        unique=True,
    )
    bio = models.TextField(blank=True)
    objects = CustomUserManager()

    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        ordering = ('id',)


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True, blank=True,)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(max_length=50, unique=True, blank=True,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name[:50]


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название',
        blank=False, null=False
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=True, null=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        blank=True, null=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='category'
    )
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    def __str__(self):
        return self.name[:50]


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(User, models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, 'минимальная оценка 1'),
            MaxValueValidator(10, 'максимальная оценка 10')
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    title = models.ForeignKey(Title, models.CASCADE, related_name='reviews')

    """class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='constraints_review')
        ]"""
    
    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(User, models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    review = models.ForeignKey(Review, models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text