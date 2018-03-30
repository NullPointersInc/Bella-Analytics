# Generated by Django 2.0.3 on 2018-03-30 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryDevice',
            fields=[
                ('device_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='devices.Device')),
                ('state', models.IntegerField(choices=[(0, 'Off'), (1, 'On')], default=0)),
            ],
            bases=('devices.device',),
        ),
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('controller_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('controller_type', models.CharField(choices=[('T', 'Temperature'), ('L', 'Luminosity')], default='T', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='FuzzyDevice',
            fields=[
                ('device_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='devices.Device')),
                ('state', models.IntegerField(choices=[(0, 'Off'), (1, 'Low'), (2, 'High')], default=0)),
            ],
            bases=('devices.device',),
        ),
        migrations.RemoveField(
            model_name='device',
            name='usage_number',
        ),
        migrations.RemoveField(
            model_name='device',
            name='wattage',
        ),
        migrations.AddField(
            model_name='device',
            name='controller',
            field=models.ForeignKey(default='T', on_delete=django.db.models.deletion.CASCADE, to='devices.Controller'),
            preserve_default=False,
        ),
    ]
