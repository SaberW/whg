# Generated by Django 2.1.2 on 2018-10-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0002_auto_20181023_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='datatype',
            field=models.CharField(choices=[('place', 'Places'), ('anno', 'Annotations')], default='place', max_length=12),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='format',
            field=models.CharField(choices=[('csv', 'Simple CSV'), ('lpf', 'Linked Places format')], default='csv', max_length=12),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.CharField(blank=True, choices=[('format_error', 'Invalid format'), ('format_ok', 'Valid format'), ('uploaded', 'Uploaded'), ('ready', 'Ready for submittal'), ('accepted', 'Accepted')], max_length=12, null=True),
        ),
    ]