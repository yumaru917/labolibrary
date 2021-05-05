from django.urls import path
from . import views

app_name = 'data_upload'
urlpatterns = [
    # :
    # :
    path('data_upload/', views.upload, name='upload'),
    # :
    # :
]