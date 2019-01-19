# Generated by Django 2.1.4 on 2018-12-30 11:55

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_cacheddata'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bbox', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
                ('zoom_min', models.FloatField()),
                ('zoom_max', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Narration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('date_label', models.CharField(max_length=100)),
                ('map_datetime', models.DateTimeField()),
                ('img', models.URLField(blank=True, null=True)),
                ('video', models.URLField(blank=True, null=True)),
                ('attached_events', models.ManyToManyField(to='api.CachedData')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Narrative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
            ],
        ),
        migrations.AddField(
            model_name='narration',
            name='narrative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Narrative'),
        ),
        migrations.AddField(
            model_name='narration',
            name='settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.MapSettings'),
        ),
    ]