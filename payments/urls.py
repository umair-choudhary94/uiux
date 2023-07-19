from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('credits/', views.credits, name='credits'),
    path('subscription/', views.subscriptions, name='subscription'),
    path('payments/', views.payments, name='payments'),
    path('wallet/', views.wallet, name='wallet'),
    path("withdraw/", views.withdraw,name="withdraw"),
    path("payment-history/", views.payment_history,name="payment-history"),
    path("income/", views.income,name="income"),
    path("payment-information-card/", views.payment_information1, name="payment-information-card"),
    path("payment-information-paypal/", views.payment_information2,name="payment-information-paypal"),

]