from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreateHome.as_view(), name='user_create_home'),
    path('user_create/university', views.register_university, name='university_create'),

    # 本番は削除する。（都道府県の登録が終わったら。）
    path('user_create/university_area', views.register_university_area, name='university_area_create'),

    path('user_create/faculty', views.register_faculty, name='faculty_create'),
    path('user_create/department', views.register_department, name='department_create'),
    path('user_create/laboratory', views.register_laboratory, name='laboratory_create'),
    path('user_create/lab/', views.LabUserCreate.as_view(), name='lab_user_create'),
    path('user_create/student/', views.StudentUserCreate.as_view(), name='student_user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),

    path('user_delete/confirm', views.user_delete_confirm, name='user_delete_confirm'),
    path('user_delete', views.UserDeleteView.as_view(), name='user_delete'),
]
