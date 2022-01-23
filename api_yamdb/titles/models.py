from django.db import models
from pytils.translit import slugify


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True, blank=True,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)


class Genre(Category):
    pass


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название',
        blank=False, null=False
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=True, null=True
    )
    raiting = models.IntegerField(
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
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='genre'
    )
