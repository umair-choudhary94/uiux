from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="home"),
    path("create-new-post/", views.new_post),
    path("bookmark/", views.isbookmark, name="bookmark"),
    path("like/", views.islike,name="like"),
    path("bookmarks/",views.bookmarks,name="bookmarks"),
    path("likedpost/",views.likedpost,name="likedpost"),
    path("notifications/",views.notifications, name="notifications"),
    path("profile/", views.myprofile),
    path("edit-profile/", views.edit_profile),
    path('comment/', views.comments, name='comment'),
    path("chat/", views.chat),
]