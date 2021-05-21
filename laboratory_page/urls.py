from search_lab import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
import register_lab

app_name = 'laboratory_page'
urlpatterns = [
    path('', views.lab_page, name='lab_page_home'),
    path('laboratory_fovorite_user/<int:pk>', views.favorite_user_profile, name='laboratory_favorite_user'),
    path('notification/<int:pk>', views.notification_detail, name='notification'),
    path('<int:pk>/labdata_update/', register_lab.views.LabInfoUpdate.as_view(), name='labdata_update'),
    path('lab_info_delete', views.LabInfoDeleteView.as_view(), name='lab_info_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
