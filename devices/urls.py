from django.urls import path
from . import views

urlpatterns = [
    #path('getprices/', views.getPrices, name="getprices"),
    path('devices/', views.devices, name="devices"),
    #path('devices/update_device/<str:pk>/', views.receive_data, name="receive_data"),
    path('devices/device_graph/<str:pk>/', views.device_history, name="device_history"),
    path('devices/<str:pk>/', views.device_PL, name="device_pl"),
]