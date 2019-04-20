# Generated by Django 2.2 on 2019-04-19 03:14

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190418_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmapsettings',
            name='bbox',
        ),
        migrations.RemoveField(
            model_name='mapsettings',
            name='bbox',
        ),
        migrations.AddField(
            model_name='historicalnarration',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='narration',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
