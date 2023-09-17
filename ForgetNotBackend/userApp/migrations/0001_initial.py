# Generated by Django 4.1.5 on 2023-02-26 15:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("email", models.CharField(max_length=128, unique=True)),
                ("birthday", models.DateTimeField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "male"), ("female", "female")],
                        default="female",
                        max_length=6,
                    ),
                ),
                ("firstName", models.CharField(blank=True, max_length=32)),
                ("lastName", models.CharField(blank=True, max_length=32)),
                ("is_active", models.BooleanField(default=False)),
                ("last_login", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={"abstract": False, },
        ),
        migrations.CreateModel(
            name="Label",
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
                ("name", models.CharField(max_length=64)),
                ("color", models.CharField(max_length=64)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
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
                ("title", models.CharField(max_length=256)),
                ("description", models.CharField(blank=True, max_length=1024)),
                ("startTime", models.DateTimeField()),
                ("endTime", models.DateTimeField()),
                (
                    "type",
                    models.IntegerField(
                        choices=[(0, "all day"), (1, "repeat")], default=0
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="userApp.label"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]