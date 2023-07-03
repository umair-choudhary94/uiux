from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    # path('messages/', views.my_messages, name='messages'),
    # path('privacy/', views.privacy, name='privacy'),
    # path('settings/', views.account_settings, name='account-settings'),
]