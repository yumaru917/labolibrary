from django.urls import path
from . import views

app_name = 'feedback'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('send_feedback_success', views.SendFeedbackSuccessView.as_view(), name='send_feedback_success'),
]
