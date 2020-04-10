"""BBS_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.views.static import serve
from app1 import views
from BBS_Blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('get_valid_image/', views.get_valid_image),
    path('index/', views.index),
    path('logout/', views.logout),
    path('register/', views.register),
    path('digg/', views.digg),
    re_path(r'^(?P<username>\w+)$', views.home_site),
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|date)/(?P<param>.*)/$', views.home_site),
    re_path(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/$', views.article_detail),
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]
