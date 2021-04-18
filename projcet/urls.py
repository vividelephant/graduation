"""projcet URL Configuration

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
from django.urls import path
from Cat import views
from django.conf.urls import url
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.user_login),
    path('home/',views.home),
    # path('index/', views.index),
    # path('calpage/',views.calpage),
    # path('calculate/',views.calculate,name='calculate'),
    # path('list/',views.callist),
    # path('del/',views.deldata,name='del'),
    # path('', views.index, name='index'),#
    # path('',views.login),
    path('index/',views.index,name = 'index'),
    path('user_login/',views.user_login,name = 'user_login'),
    path('forgot_password/',views.forgot_password,name = 'forget_password'),
    path('register/',views.register,name = 'register'),
    path('user_logout/',views.user_logout,name = 'user_logout'),
    path('table/',views.client_table,name = 'client_table'),
    path('user_manage/',views.user_manage,name = 'user_manage'),
    path('add_user/', views.add_user, name = 'add_user'),
    path('delete_user/',views.delete_user,name = 'delete_user'),
    path('change_user/',views.change_user,name='change_user'),
    path('safe_clients/',views.safe_clients,name = 'safe_clients'),
]