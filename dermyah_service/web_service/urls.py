from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wifi', views.wifi, name='wifi'),
    path('login', views.login, name='login'),
    path('login_admin', views.login_admin, name='login_admin'),
    path('connect', views.connect, name='connect'),
    path('reset', views.reset, name='reset'),
    path('arduino', views.arduino, name='arduino'),
    path('mainPage', views.mainPage, name='mainPage')
]
