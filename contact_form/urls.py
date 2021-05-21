from django.urls import path
from . import views

app_name = 'contact_form'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('send_contact_success', views.SendContactSuccessView.as_view(), name='send_contact_success'),
]
