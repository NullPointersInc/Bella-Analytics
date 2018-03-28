from django.db import models

# Create your models here.

class LoggedData(models.Model):
    timestamp = models.BigIntegerField()
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE)
    value = models.IntegerField()
