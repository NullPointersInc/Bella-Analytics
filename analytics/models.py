from django.db import models

# Create your models here.

class LoggedDeviceData(models.Model):
    timestamp = models.BigIntegerField()
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    state = models.CharField(max_length=16,default='off')

class LoggedRoomData(models.Model):
    timestamp = models.BigIntegerField()
    hum_value = models.FloatField(default=0)
    temp_value = models.FloatField(default=0)
    lux_value = models.FloatField(default=0)
