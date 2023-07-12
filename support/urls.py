from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("customer-support/", views.customer_support, name="customer-support"),
    path("terms-and-conditions/", views.terms_condition, name="terms-and-conditions"),
    path("blocked-user/", views.blocked_user,name="blocked-user"),
    path("unblock-user/<int:user_id>/", views.unblocked_user,name="unblock-user"),
    # path('messages/', views.my_messages, name='messages'),
    # path('privacy/', views.privacy, name='privacy'),
    # path('settings/', views.account_settings, name='account-settings'),
]