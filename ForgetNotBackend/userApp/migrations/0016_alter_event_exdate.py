# Generated by Django 4.1.7 on 2023-03-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userApp", "0015_event_exdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="exDate",
            field=models.CharField(blank=True, default="", max_length=1024, null=True),
        ),
    ]