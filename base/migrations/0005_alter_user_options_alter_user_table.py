# Generated by Django 5.0 on 2023-12-17 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_remove_film_author_film_director_film_duration_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(name="user", options={},),
        migrations.AlterModelTable(name="user", table="auth_user",),
    ]