# Generated by Django 4.1.7 on 2023-03-05 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("userApp", "0002_user_is_visitor"),
    ]

    operations = [
        migrations.RemoveField(model_name="event", name="label",),
        migrations.RemoveField(model_name="event", name="owner",),
        migrations.CreateModel(
            name="Event_User_Relation",
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
                (
                    "type",
                    models.IntegerField(
                        choices=[(0, "owner"), (1, "invitee")], default=0
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "pending"), (1, "accept"), (2, "Rejection")],
                        default=0,
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="userApp.event"
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="userApp.label"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
