from allauth.socialaccount.providers import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import *
from uiapp.models import *
from django.db import connection
import stripe
from  django.conf import settings
from django.views import View
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def SuccessView(request):
    context ={}
    return render(request, "landing.html", context)


def CancelView(request):
    context ={}
    return render(request, "landing.html", context)


def PaymentLandingPageView(request):
    context ={}
    return render(request, "landing.html", context)

# class CreateCheckoutSessionView(View):
def CreateCheckoutSessionView(request):
        try:
            YOUR_DOMAIN = "http://127.0.0.1:8000/payments"
            checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items =[{
            'price_data' :{
            'currency' : 'usd',
            'unit_amount': 2000,
                'product_data': {
                  'name': 'uiux',
                },
                },
                'quantity' : 1
              }],
                mode= 'payment',
                success_url= YOUR_DOMAIN +'/success/',
                cancel_url= YOUR_DOMAIN + '/cancel/',
                )
            # return JsonResponse({'id': checkout_session.id})
            print(checkout_session);
            return redirect(checkout_session.url)
        except Exception as e:
            return e

def credits(request):
    return render(request,"wallet.html")
def wallet(request):
    return render(request,"wallet.html")

def withdraw(request):
    return render(request,"withdraw.html")

def payment_history(request):
    return render(request,"paymenthistory.html")

def income(request):
    return render(request,"income.html")

@login_required(login_url='/login')
def payment_information1(request):
    if request.method == 'POST':
        data = request.POST
        email =  data.get('email')
        paymentDetail = PaymentInformation.objects.filter(email = email).first()
        if paymentDetail is None:
            paymentModel = PaymentInformation()
            paymentModel.email = data.get('email')
            paymentModel.payment_method = data.get('payment_method')
            paymentModel.card_information = data.get('card_information')
            paymentModel.card_date = data.get('card_date')
            paymentModel.card_cvc = data.get('card_cvc')
            paymentModel.card_owner_name = data.get('card_owner_name')
            paymentModel.country = data.get('country')
            paymentModel.address = data.get('address')
            paymentModel.user_id = request.user.id
            paymentModel.save()
        else:
            paymentDetail.email = data.get('email')
            paymentDetail.payment_method = data.get('payment_method')
            paymentDetail.card_information = data.get('card_information')
            paymentDetail.card_date = data.get('card_date')
            paymentDetail.card_cvc = data.get('card_cvc')
            paymentDetail.card_owner_name = data.get('card_owner_name')
            paymentDetail.country = data.get('country')
            paymentDetail.address = data.get('address')
            paymentDetail.user_id = request.user.id
            paymentDetail.save()
        profilepic = Profile.objects.filter(id=request.user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
        accountDetail = PaymentInformation.objects.filter(user_id = request.user.id).first()
        context = {'user': request.user, 'user_id': request.user.id, 'accountDetail': accountDetail, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
        return render(request,"uiapp/accountdatail.html", context)
    else:
        profilepic = Profile.objects.filter(id=request.user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
        accountDetail = PaymentInformation.objects.filter(user_id = request.user.id)
        context = {'user': request.user, 'user_id': request.user.id, 'accountDetail': accountDetail, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
        return render(request,"paymentinfo1.html", context)

def payment_information2(request):
    if request.method == 'POST':
        stripe.api_key = "sk_test_51NVfDWLmNf9m8AAUUpnsHyOwrN2eEGaIneQmmw9pD1EFTzH1oy951pNdtXBCITUf04YxwGMuak6LTL6GxoUFCIMA00O1AidHMl";
        customer = stripe.Customer.create(
            email = request.user.email
        )
        charge = stripe.Charge.create(
            customer = customer,
            amount = 20,
            currency = "usd",
            description = "Membership"

        )
    return render(request,"paymentinfo2.html")

def subscriptions(request):
    id = request.user.id
    user = SubscribeBlockUser.objects.filter(user_id=id).first()
    if user:
        if user.is_subscribed == 'True':
            user.is_subscribed = False
            user.save()
        else:
            user.is_subscribed = True
            user.save()
    else:
        userModel = SubscribeBlockUser()
        userModel.user_id = id
        userModel.is_subscribed = True
        userModel.is_blocked = False
        userModel.save()
    profile = Profile.objects.filter(user_id=id)
    user = request.user
    post = Post.objects.filter(user_id=request.user.id)
    context = {'user': user, 'post': post, 'profile': profile}
    return render(request,"subscription.html",context)