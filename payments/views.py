import datetime

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
from datetime import date
stripe.api_key = settings.STRIPE_SECRET_KEY
from datetime import timedelta
@login_required(login_url='/login')
def SuccessView(request, creator_id):
    subscription = SubscribeUser.objects.filter(creator_id=request.user.id).first()
    if subscription:
        if subscription.is_subscribed == 'False':
            subscription.is_subscribed = True
            origin_date = datetime.today()
            end_time = origin_date + timedelta(days=30)
            subscription.end_date = end_time
            subscription.creator_id = creator_id
            subscription.subscriber_id = request.user.id
            subscription.save()
        else:
            subscription.is_subscribed = False
            subscription.end_date = datetime.today()
            subscription.save()
    else:
        userModel = SubscribeUser()
        userModel.is_subscribed = True
        origin_date = datetime.today()
        end_time = origin_date + timedelta(days=30)
        userModel.end_date = end_time
        userModel.creator_id = creator_id
        userModel.subscriber_id = request.user.id
        userModel.save()
    subscriptions = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic, " \
            "lb.subscriber_id, lb.creator_id, lb.start_date, lb.end_date " \
            "FROM user_user u " \
            "FULL JOIN user_profile pro ON u.id = pro.user_id " \
            "LEFT JOIN payments_subscribeuser lb ON pro.user_id = lb.subscriber_id "\
            "WHERE lb.is_subscribed = 'TRUE' AND lb.subscriber_id = " + str(request.user.id);
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        subscriptions.append(row_dict)
    profile = Profile.objects.filter(user_id=request.user.id)
    post = Post.objects.filter(user_id=request.user.id)
    context = {'user': request.user, 'post': post, 'profile': profile, 'subscriptions': subscriptions}
    return render(request, "subscription.html", context)


def CancelView(request):
    context ={}
    return render(request, "landing.html", context)
@login_required(login_url='/login')
def ServicesPageView(request):
    if request.method == 'POST':
        data = request.POST
        email =  data.get('email')
        serviceDetail = Product.objects.filter(user_id = request.user.id).first()
        if serviceDetail is None:
            serviceModel = Product()
            serviceModel.product_name = data.get('product_name')
            serviceModel.product_desc = data.get('product_desc')
            serviceModel.product_price = data.get('product_price')
            serviceModel.currency = data.get('currency')
            serviceModel.user_id = request.user.id
            serviceModel.save()
        else:
            serviceDetail.product_name = data.get('product_name')
            serviceDetail.product_desc = data.get('product_desc')
            serviceDetail.product_price = data.get('product_price')
            serviceDetail.currency = data.get('currency')
            serviceDetail.user_id = request.user.id
            serviceDetail.save()
        profilepic = Profile.objects.filter(id=request.user.id).first()
        services = Product.objects.filter(user_id = request.user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
        accountDetail = PaymentInformation.objects.filter(user_id = request.user.id).first()
        context = {'user': request.user, 'services':services, 'user_id': request.user.id, 'accountDetail': accountDetail, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
        return render(request,"product.html", context)
    else:
        profilepic = Profile.objects.filter(id=request.user.id).first()
        services = Product.objects.filter(user_id=request.user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id=request.user.id).count()
        accountDetail = PaymentInformation.objects.filter(user_id=request.user.id).first()
        context = {'user': request.user, 'services': services, 'user_id': request.user.id, 'accountDetail': accountDetail,
                   'profilepic': profilepic.profilepic, 'notification_count': notification_count}
        return render(request, "product.html", context)

def PaymentLandingPageView(request):
    context ={}
    return render(request, "landing.html", context)

@login_required(login_url='/login')
def CreateCheckoutSessionView(request, creator_id):
        try:
            YOUR_DOMAIN = "http://127.0.0.1:8000/payments";
            services = Product.objects.get(user_id=request.user.id)
            checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items =[{
            'price_data' :{
            'currency' : services.currency,
            'unit_amount': 200*(services.product_price),
                'product_data': {
                'name': services.product_name,
                'description': services.product_desc,
                },
                },
                'quantity' : 1
              }],
                mode= 'payment',
                success_url= YOUR_DOMAIN +'/success/'+str(creator_id),
                cancel_url= YOUR_DOMAIN + '/cancel/',
                )
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
            prod_id = Product.objects.filter(user_id = request.user.id).first()
            paymentModel.product_id = prod_id.id
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
            prod_id = Product.objects.filter(user_id = request.user.id).first()
            paymentDetail.product_id = prod_id.id
            paymentDetail.save()
        profilepic = Profile.objects.filter(id=request.user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
        accountDetail = PaymentInformation.objects.filter(user_id = request.user.id).first()
        context = {'user': request.user, 'user_id': request.user.id, 'accountDetail': accountDetail, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
        return render(request,"uiapp/accountdetail.html", context)
    else:
        profilepic = Profile.objects.filter(id=request.user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
        accountDetail = PaymentInformation.objects.filter(user_id = request.user.id).first()
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
    subscriptions = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic, " \
            "lb.subscriber_id, lb.creator_id, lb.start_date, lb.end_date " \
            "FROM user_user u " \
            "FULL JOIN user_profile pro ON u.id = pro.user_id " \
            "LEFT JOIN payments_subscribeuser lb ON pro.user_id = lb.subscriber_id "\
            "WHERE lb.is_subscribed = 'TRUE' AND lb.subscriber_id = " + str(request.user.id);
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        subscriptions.append(row_dict)
    profile = Profile.objects.filter(user_id=request.user.id)
    post = Post.objects.filter(user_id=request.user.id)
    context = {'user': request.user, 'post': post, 'profile': profile, 'subscriptions': subscriptions}
    return render(request, "subscription.html", context)