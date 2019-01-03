# Generated by Django 2.1.2 on 2019-01-02 17:43

import django.contrib.postgres.fields
from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0003_auto_20190101_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='ccodes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='area',
            name='geom',
            field=djgeojson.fields.PolygonField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='area',
            name='type',
            field=models.CharField(choices=[('ccodes', 'Country codes'), ('region', 'Region/Polity record'), ('user', 'User drawn')], max_length=20),
        ),
    ]
