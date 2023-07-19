from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import *
from uiapp.models import *
from django.db import connection

# Create your views here.

def credits(request):
    return render(request,"wallet.html")

def payments(request):
    return render(request,"paymentinfo1.html.html")
def wallet(request):
    return render(request,"wallet.html")

def withdraw(request):
    return render(request,"withdraw.html")

def payment_history(request):
    return render(request,"paymenthistory.html")

def income(request):
    return render(request,"income.html")

def payment_information1(request):
    return render(request,"paymentinfo1.html")

def payment_information2(request):
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