from django.urls import path
from . import views

urlpatterns = {
    path('elspot/', views.getPrices, name="elspot"),
}