from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.search_view, name='search'),
    path('<int:lab_pk>/', views.detail_view, name='detail'),
]
