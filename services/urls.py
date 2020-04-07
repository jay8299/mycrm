"""myCMP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user_page"),
    path('account/', views.account_settings, name="account"),
    path('',views.home,name="home"),

    path('products/', views.product, name="product"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('createorder/<str:pk>/', views.create_order, name="create_order"),
    path('updateorder/<str:pk>/', views.update_order, name="update_order"),
    path('deleteorder/<str:pk>/', views.delete_order, name="delete_order"),


]
