# Generated by Django 4.2.8 on 2024-02-29 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0009_alter_film_video_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(default="avatar.svg", null=True, upload_to=""),
        ),
    ]