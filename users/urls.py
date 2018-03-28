from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/<username>', views.get_user, name='get_user'),
    path('all', views.get_all, name='get_all'),
    path('new', views.create_user, name='create_user')
]
