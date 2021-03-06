"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path,re_path
from users import views as user_views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'',include('images.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('update_profile/', user_views.update_profile, name='update_profile'),
    path('upload_image/', user_views.upload_image, name='upload_image'),
    url(r'^like/(?P<operation>.+)/(?P<pk>\d+)',user_views.like, name='like'),
    re_path(r'^comment/(?P<pk>\d+)', user_views.add_comment, name='comment'),

    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('search/', user_views.search_users, name='search'),
    url(r'^follow/(?P<operation>.+)/(?P<id>\d+)',user_views.follow,name='follow'),


]
