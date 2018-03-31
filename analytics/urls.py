from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log', views.log_data, name='log_data'),
    path('get/graph/device/<device_id>', views.get_device_graph, name='get_device_graph'),
    path('log_data_live', views.handle_live_data, name='handle_live_data'),
    path('update_success', views.update_success, name='update_success'),
    path('get_usage_stats', views.get_stats, name='usage_stats'),
    path('detect_anomaly', views.perform_anomaly_detection, name='perform_anomaly_detection')
]
