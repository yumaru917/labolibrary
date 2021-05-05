from django.urls import path
from . import views

app_name = 'contact_form'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
