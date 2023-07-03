from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('notifications/', views.notifications, name='notifications'),


]