# Generated by Django 5.0.6 on 2024-09-15 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0004_alter_statistic_device_os"),
    ]

    operations = [
        migrations.AddField(
            model_name="statistic",
            name="custom_params",
            field=models.JSONField(null=True),
        ),
        migrations.CreateModel(
            name="TrackingParams",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("params", models.CharField(max_length=20)),
                (
                    "shortened_url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shortener.shortenedurls",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
