# Generated by Django 2.1.2 on 2018-12-24 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20181224_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='src_id',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]