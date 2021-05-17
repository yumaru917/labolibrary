from django.urls import path
from . import views

app_name = 'mypage'
urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('profile', views.user_profile, name='user_profile'),
    path('create_user_profile', views.create_user_profile, name='create_user_profile'),
    # 要修正（エラー原因）
    path('<int:pk>/user_profile_update', views.UserProfileUpdate.as_view(), name='user_profile_update'),
]
