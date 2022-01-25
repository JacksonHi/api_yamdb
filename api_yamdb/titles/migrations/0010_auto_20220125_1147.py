# Generated by Django 2.2.16 on 2022-01-25 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0009_auto_20220124_1644'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='titlegenre',
            constraint=models.UniqueConstraint(fields=('genre', 'title'), name='unique_genre_title'),
        ),
    ]
