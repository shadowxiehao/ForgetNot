# Generated by Django 4.1.7 on 2023-03-17 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userApp", "0013_alter_event_enddate_alter_event_startdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="notes",
            field=models.CharField(blank=True, default="", max_length=1024),
        ),
    ]