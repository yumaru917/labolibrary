from django.urls import path
from . import views
import register_lab

app_name = 'mypage'
urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('<int:pk>/labdata_update/', register_lab.views.LabInfoUpdate.as_view(), name='labdata_update'),
]
