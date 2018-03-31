from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/devices/<device_id>', views.get_device, name='get_device'),
    path('all/devices', views.get_all_devices, name='get_all_devices'),
    path('new/device', views.create_device, name='create_device'),
    path('delete/devices/<device_id>', views.delete_device, name='delete_device'),
]
