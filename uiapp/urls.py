from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    path("",views.signup),
    path("create-new-post/", views.new_post),
    path("bookmark/<int:post_id>/", views.isbookmark, name="bookmark"),
    path("like/<int:post_id>/", views.islike,name="like"),
    path("bookmarks/",views.bookmarks),
    path("likedpost/",views.likedpost),
    path("notifications/",views.notifications),
    path("subscription/",views.subscription),
    path("wallet/",views.wallet),
    path("withdraw/",views.withdraw),
    path("payment-history/",views.payment_history),
    path("income/", views.income),
    path("payment-information-card/", views.payment_information1),
    path("payment-information-paypal/", views.payment_information2),
    path("profile/", views.myprofile),
    path("edit-profile/", views.edit_profile),
    path("chat/", views.chat),
]