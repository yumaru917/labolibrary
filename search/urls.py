from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.search_view, name='search'),
    path('tag_search', views.tag_search_view, name='tag_search'),
    path('<int:lab_pk>/', views.detail_view, name='detail'),
    path('<int:lab_pk>/send_message_for_lab', views.send_message_for_laboratory_view, name='send_message_for_lab'),
    path('<int:pk>/paper_download/', views.paper_download, name='paper_download'),
    path('follow/<int:pk>/', views.follow_laboratory, name='follow'),
    path('remove_follow/<int:pk>/', views.remove_follow_laboratory, name='remove_follow'),
]
