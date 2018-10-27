# Generated by Django 2.1.2 on 2018-10-25 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0003_auto_20181024_1948'),
        ('main', '0007_auto_20181023_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='placename',
            name='dataset',
            field=models.ForeignKey(db_column='dataset', default='', on_delete='models.CASCADE', to='contribute.Dataset', to_field='label'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='placename',
            name='src_id',
            field=models.CharField(default='', max_length=24),
            preserve_default=False,
        ),
    ]
