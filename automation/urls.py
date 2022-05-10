from django.urls import path
from . import views

urlpatterns = {
    path('devices/update_device/<str:pk>/', views.receive_data, name="receive_data"),
}