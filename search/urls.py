from django.urls import path
from . import views
from search_lab import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'search'
urlpatterns = [
    path('', views.search_view, name='search'),
    path('tag_search', views.tag_search_view, name='tag_search'),
    path('<int:lab_pk>/', views.detail_view, name='detail'),
    path('<int:lab_pk>/research_paper_list', views.research_paper_list_view, name='research_paper_list'),
    path('<int:lab_pk>/send_message_for_lab', views.send_message_for_laboratory_view, name='send_message_for_lab'),
    path('<int:pk>/paper_download/', views.paper_download, name='paper_download'),
    path('follow/<int:pk>/', views.follow_laboratory, name='follow'),
    path('remove_follow/<int:pk>/', views.remove_follow_laboratory, name='remove_follow'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
