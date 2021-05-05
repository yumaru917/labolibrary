from django.urls import path
from . import views

app_name = 'register_lab'
urlpatterns = [
    path('', views.register_lab, name='register'),
]
