# Generated by Django 2.0.3 on 2018-03-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=64)),
                ('full_name', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
