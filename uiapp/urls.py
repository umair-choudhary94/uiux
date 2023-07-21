from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="home"),
    path("create-new-post/", views.new_post),
    path("bookmark/", views.isbookmark),
    path("like/", views.islike),
    path("bookmarks/",views.bookmarks,name="bookmarks"),
    path("likedpost/",views.likedpost,name="likedpost"),
    path("notifications/",views.notifications, name="notifications"),
    path("readnotification/",views.read_notification, name="readnotification"),
    path("profile/", views.myprofile),
    path("edit-profile/", views.edit_profile),
    path('comment/', views.comments, name='comment'),
    path("chat/", views.chat),
]