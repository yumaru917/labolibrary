from search_lab import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'register_lab'
urlpatterns = [
    path('', views.register_lab, name='register'),
    path('paper_upload', views.paper_upload, name='paper_upload'),
    path('<int:pk>/paper_delete/', views.PaperDelete.as_view(), name='paper_delete'),
    path('image_upload', views.image_upload, name='image_upload'),
    path('<int:pk>/image_delete/', views.ImageDelete.as_view(), name='image_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
