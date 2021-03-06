# Generated by Django 2.0.3 on 2018-03-30 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20180330_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='binarydevice',
            name='next_state',
            field=models.IntegerField(choices=[(0, 'Off'), (1, 'On')], default=0),
        ),
        migrations.AddField(
            model_name='fuzzydevice',
            name='next_state',
            field=models.IntegerField(choices=[(0, 'Off'), (1, 'Low'), (2, 'High')], default=0),
        ),
    ]
