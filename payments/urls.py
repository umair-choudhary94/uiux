from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('credits/', views.credits, name='credits'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('payments/', views.payments, name='payments'),
    path('wallet/', views.wallet, name='wallet'),

]