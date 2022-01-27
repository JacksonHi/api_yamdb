from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User









class Review(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, 'минимальная оценка 1'),
            MaxValueValidator(10, 'максимальная оценка 10')
        ]
    )
    pub_date = models.DateTimeField(verbose_name='дата публикации', auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='constraints_review')
        ]
    
    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField('текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(verbose_name='дата публикации', auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text