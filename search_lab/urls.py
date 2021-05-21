"""search_lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from search_lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', views.index, name='index'),
    path('index_for_lab', views.index_for_lab, name='index_for_lab'),
    path('disclaimer', views.disclaimer, name='disclaimer'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service', views.terms_of_service, name='terms_of_service'),
    path('about', views.about, name='about'),
    path('about_administrator', views.about_administrator, name='about_administrator'),
    path('about/lab', views.about_for_laboratory, name='about_for_laboratory'),
    path('upload/', include('data_upload.urls')),  # 今回追加
    path('search/', include('search.urls')),  # 今回追加
    path('register/', include('register_lab.urls')),  # 今回追加
    path('contact/', include('contact_form.urls')),  # 今回追加
    path('feedback/', include('feedback.urls')),  # 今回追加
    path('mypage/', include('mypage.urls')),  # 今回追加
    path('blog/', include('blog.urls')),  # 今回追加
    path('articles/', include('articles.urls')),  # 今回追加
    path('laboratory_page/', include('laboratory_page.urls')),  # 今回追加
    path('chat/', include('chat.urls')),  # 今回追加
]
