# Generated by Django 4.2.6 on 2023-11-21 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="film_videos"),
        ),
    ]
