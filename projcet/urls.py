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

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.index ),
    # path('index/', views.index),
    # path('calpage/',views.calpage),
    # path('calculate/',views.calculate,name='calculate'),
    # path('list/',views.callist),
    # path('del/',views.deldata,name='del'),
    # path('', views.index, name='index'),#
    # path('',views.login),
    path('index/',views.index,name = 'index'),
    path('user_login/',views.user_login,name = 'login'),
    path('forgot_password/',views.forgot_password,name = 'forget_password'),
    path('register/',views.register,name = 'register')

]
