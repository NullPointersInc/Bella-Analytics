from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/devices/<device_id>', views.get_device, name='get_device'),
    path('get/rooms/<room_id>', views.get_room, name='get_room'),
    path('all/devices/<room_id>', views.get_all_devices, name='get_all_devices'),
    path('all/rooms', views.get_all_rooms, name='get_all_rooms'),
    path('new/device', views.create_device, name='create_device'),
    path('new/room', views.create_room, name='create_room'),
    path('delete/rooms/<room_id>', views.delete_room, name='delete_room'),
    path('delete/devices/<device_id>', views.delete_device, name='delete_device'),
]
