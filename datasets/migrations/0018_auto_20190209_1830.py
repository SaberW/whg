# Generated by Django 2.1.2 on 2019-02-09 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0017_auto_20190130_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='uri_base',
            field=models.URLField(blank=True, null=True),
        ),
        #migrations.AlterField(
            #model_name='hit',
            #name='place_id',
            #field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place'),
        #),
    ]
