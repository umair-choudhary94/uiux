from django.urls import path
from django.conf.urls import url
from . import views
from .views import PaymentLandingPageView, CancelView, SuccessView

urlpatterns = [
    path('credits/', views.credits, name='credits'),
    path('subscription/', views.subscriptions, name='subscription'),
    # path('payments/', views.payments, name='payments'),
    path('wallet/', views.wallet, name='wallet'),
    path("withdraw/", views.withdraw,name="withdraw"),
    path("payment-history/", views.payment_history,name="payment-history"),
    path("income/", views.income,name="income"),
    path("payment-information-card/", views.payment_information1, name="payment-information-card"),
    path("payment-information-paypal/", views.payment_information2,name="payment-information-paypal"),
    # path("create-checkout-session/<pk>/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    # path("create-payment-intent/<pk>/", CreateCheckoutSessionView.as_view(), name="create-payment-intent"),
    path("landingpage/", views.PaymentLandingPageView, name="landingpage"),
    path("checkout/<int:creator_id>/", views.CreateCheckoutSessionView, name="checkout"),
    path("cancel/", views.CancelView, name="cancel"),
    path("success/<int:creator_id>/", views.SuccessView, name="success"),
    path('services/', views.ServicesPageView, name='services'),
]