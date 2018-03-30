from django.db import models

# Create your models here.

class LoggedDeviceData(models.Model):
    timestamp = models.BigIntegerField()
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    state = models.CharField(max_length=16,default='off')

class LoggedRoomData(models.Model):
    timestamp = models.BigIntegerField()
    room = models.ForeignKey('devices.Room', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
