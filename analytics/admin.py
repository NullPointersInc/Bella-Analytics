from django.contrib import admin
from .models import LoggedDeviceData, LoggedRoomData

# Register your models here.

admin.site.register(LoggedDeviceData)
admin.site.register(LoggedRoomData)
