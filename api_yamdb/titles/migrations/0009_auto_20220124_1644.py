# Generated by Django 2.2.16 on 2022-01-24 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0008_auto_20220124_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='titles.TitleGenre', to='titles.Genre'),
        ),
        migrations.AlterField(
            model_name='titlegenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='titles.Genre'),
        ),
        migrations.AlterField(
            model_name='titlegenre',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='titles.Title'),
        ),
    ]
