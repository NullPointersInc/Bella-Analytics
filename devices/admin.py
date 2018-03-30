from django.contrib import admin

from .models import Room, Device, FuzzyDevice, BinaryDevice
# Register your models here.

admin.site.register(Room)
admin.site.register(Device)
admin.site.register(FuzzyDevice)
admin.site.register(BinaryDevice)
