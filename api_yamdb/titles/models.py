from django.db import models
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True, blank=True,)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name[:50])
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(max_length=50, unique=True, blank=True,)

    def __str__(self):
        return self.name[:50]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name[:50])
        super().save(*args, **kwargs)


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
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name[:50]