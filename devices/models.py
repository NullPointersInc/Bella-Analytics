from django.db import models

# Create your models here.

#Where do children learn?

class Device(models.Model):
    device_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=128)
    controller = models.CharField(max_length=1)
    device_type = models.CharField(max_length=1)
    mean_usage = models.FloatField(default=1.0)
    DEVICE_STATES = (
        (0, 'Off'),
        (1, 'On')
    )
    state = models.IntegerField(choices = DEVICE_STATES, default=0)
    next_state = models.IntegerField(choices = DEVICE_STATES, default=0)
