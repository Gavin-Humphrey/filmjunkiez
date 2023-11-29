# Generated by Django 4.2.7 on 2023-11-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_film_video"),
    ]

    operations = [
        migrations.RemoveField(model_name="film", name="author",),
        migrations.AddField(
            model_name="film",
            name="director",
            field=models.CharField(default="Unknown", max_length=200),
        ),
        migrations.AddField(
            model_name="film",
            name="duration",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="film",
            name="lead",
            field=models.CharField(default="Unknown", max_length=200),
        ),
        migrations.AddField(
            model_name="film",
            name="release_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
