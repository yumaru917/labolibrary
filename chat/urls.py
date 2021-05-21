from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('<int:user_pk>/', views.chat_between_user_and_user_view, name='chat_between_user_and_user'),
]
