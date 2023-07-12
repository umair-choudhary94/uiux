from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import *
from .models import *
from uiapp.models import *
# Create your views here.

@login_required(login_url='/login')
def customer_support(request):
    user = request.user
    if request.method == 'POST':
        data  = request.POST
        supportModel = CustormerSupport()
        supportModel.question = data.get('question')
        if data.get('answer') is not None:
            supportModel.answer = data.get('answer')
        else:
            supportModel.answer = ''
        supportModel.user_id = user.id
        supportModel.save()
    customer_support = CustormerSupport.objects.filter(id = user.id)
    profile = Profile.objects.filter(id = user.id).first()
    post = Post.objects.filter(user_id = user.id)
    context = {'user':user, 'profile': profile,'post':post,'customer_support':customer_support}
    return render(request,"customersupport.html", context)
@login_required(login_url='/login')
def terms_condition(request):
    return render(request,"terms.html")
@login_required(login_url='/login')
def blocked_user(request):
    id = request.user.id
    user = SubscribeBlockUser.objects.filter(user_id=id).first()
    if user:
        if user.is_blocked =='True':
            user.is_blocked = False
            user.save()
        else:
            user.is_blocked = True
            user.save()
    else:
        userModel = SubscribeBlockUser()
        userModel.user_id = id
        userModel.is_subscribed = False
        userModel.is_blocked = True
        userModel.save()
    profile = Profile.objects.filter(user_id=id)
    blocked_users = SubscribeBlockUser.objects.filter(is_blocked = True).first()
    if blocked_users is not None:
        blocked_users_list = User.objects.filter(id = blocked_users.id)
        user = request.user
        post = Post.objects.filter(user_id=request.user.id)
        context = {'user': user, 'post': post, 'profile': profile,'blocked_users':blocked_users_list}
        return render(request,"blockeduser.html",context)
    else:
        return render(request,"blockeduser.html")


@login_required(login_url='/login')
def unblocked_user(request, user_id):
    user = SubscribeBlockUser.objects.filter(user_id=user_id,is_blocked = True).first()
    if user:
        if user.is_blocked =='True':
            user.is_blocked = False
            user.save()
    id = request.user.id
    profile = Profile.objects.filter(user_id=id)
    blocked_users = SubscribeBlockUser.objects.filter(is_blocked = True).first()
    if blocked_users is not None:
        blocked_users_list = User.objects.filter(id = blocked_users.id)
        user = request.user
        post = Post.objects.filter(user_id=request.user.id)
        context = {'user': user, 'post': post, 'profile': profile,'blocked_users':blocked_users_list}
        return render(request,"blockeduser.html",context)
    else:
        return render(request,"blockeduser.html")