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
    usage_number = models.IntegerField() #Value between 0 and 16777215, can be used for advanced analytics
    wattage = models.IntegerField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

