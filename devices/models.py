from django.db import models

# Create your models here.

#Where do children learn?
class Room(models.Model):
    room_id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

class Device(models.Model):
    device_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=128)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    controller = models.CharField(max_length=1)

class FuzzyDevice(Device):
    DEVICE_STATES = (
        (0, 'Off'),
        (1, 'Low'),
        (2, 'High')
    )
    state = models.IntegerField(choices = DEVICE_STATES, default=0)
    next_state = models.IntegerField(choices = DEVICE_STATES, default=0)
    
class BinaryDevice(Device): 
    DEVICE_STATES = (
        (0, 'Off'),
        (1, 'On')
    )
    state = models.IntegerField(choices = DEVICE_STATES, default=0)
    next_state = models.IntegerField(choices = DEVICE_STATES, default=0)

