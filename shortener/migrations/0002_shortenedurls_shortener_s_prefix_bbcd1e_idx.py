# Generated by Django 5.0.6 on 2024-09-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="shortenedurls",
            index=models.Index(
                fields=["prefix", "shortened_url"], name="shortener_s_prefix_bbcd1e_idx"
            ),
        ),
    ]
