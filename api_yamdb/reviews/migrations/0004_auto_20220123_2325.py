# Generated by Django 2.2.16 on 2022-01-23 20:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220123_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'минимальная оценка 1'), django.core.validators.MaxValueValidator(10, 'максимальная оценка 10')], verbose_name='оценка'),
        ),
    ]
