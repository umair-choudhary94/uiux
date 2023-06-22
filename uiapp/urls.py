
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index),
    path("bookmarks/",views.bookmarks),
    path("likedpost/",views.likedpost),
    path("notifications/",views.notifications),
    path("subscription/",views.subscription),
    path("wallet/",views.wallet),
    path("withdraw/",views.withdraw),
    path("payment-history/",views.payment_history),
    path("income/", views.income),
    path("customer-support/", views.customer_support),
    path("terms-and-conditions/", views.terms_condition),
    path("blocked-user/", views.blocked_user),
    path("payment-information-card/", views.payment_information1),
    path("payment-information-paypal/", views.payment_information2),
    path("create-new-post/", views.new_post),
    path("my-profile/", views.myprofile),
    path("edit-profile/", views.edit_profile),
    path("chat/", views.chat),
]