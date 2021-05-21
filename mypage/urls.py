from django.urls import path
from . import views

app_name = 'mypage'
urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('profile', views.user_profile, name='user_profile'),
    path('change_favorite_laboratory_notification_confirm',
         views.change_favorite_laboratory_notification_confirm, name='change_favorite_laboratory_notification_confirm'),
    path('change_favorite_laboratory_notification_complete',
         views.change_favorite_laboratory_notification_complete, name='change_favorite_laboratory_notification_complete'),
    path('create_user_profile', views.create_user_profile, name='create_user_profile'),
    path('<int:pk>/user_profile_update', views.UserProfileUpdate.as_view(), name='user_profile_update'),
]
