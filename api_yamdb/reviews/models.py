import re
from tkinter import CASCADE
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator


from titles.models import Title

User = get_user_model()


class Review(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(User, models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'оценка',
        validators=[
            MaxLengthValidator(10, 'максимальная оценка 10'),
            MinLengthValidator(1, 'минимальная оценка 1')
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    title = models.ForeignKey(Title, models.CASCADE, related_name='reviews')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='constraints_review')
        ]
    
    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(User, models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    review = models.ForeignKey(Review, models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text
