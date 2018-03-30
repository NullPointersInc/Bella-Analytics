from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log', views.log_data, name='log_data'),
    path('get/graph/device/<device_id>', views.get_device_graph, name='get_device_graph'),
    path('get/graph/room/<room_id>', views.get_room_graph, name='get_room_graph'),
    path('log_data_live', views.handle_live_data, name='handle_live_data'),
    path('update_success', views.update_success, name='updatee_success'),
]
