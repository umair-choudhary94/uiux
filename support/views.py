from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import *
from .models import *
from uiapp.models import *
from django.db import connection

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
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user':user, 'profile': profile,'post':post,'customer_support':customer_support,'profilepic': profile.profilepic,'notification_count': notification_count}
    return render(request,"customersupport.html", context)
@login_required(login_url='/login')
def terms_condition(request):
    profile = Profile.objects.filter(id = request.user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
    context = {'profilepic': profile.profilepic,'notification_count': notification_count}
    return render(request,"terms.html",context)
@login_required(login_url='/login')
def block_user(request, user_id):
    id = request.user.id
    blocked_users = []
    user = BlockUser.objects.filter(blocked_user_id=user_id).first()
    if user:
        if user.is_blocked == True:
            user.is_blocked = False
            user.save()
        else:
            user.is_blocked = True
            user.save()
    else:
        userModel = BlockUser()
        userModel.user_id = id
        userModel.is_subscribed = False
        userModel.is_blocked = True
        userModel.blocked_user_id = user_id
        userModel.save()
        cursor = connection.cursor()
        query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic "\
                "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN user_blockuser s ON c.id = s.user_id" \
                " WHERE s.is_blocked=True AND c.id = " + str(id)
        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(col_names, row))
            blocked_users.append(row_dict)
        context = {'user_id':id,'blocked_users':blocked_users}
        return render(request,"blockeduser.html",context)
    profile = Profile.objects.filter(id = request.user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
    context = {'user_id':id,'blocked_users':blocked_users,'profilepic': profile.profilepic,'notification_count': notification_count}
    return render(request,"blockeduser.html",context)

@login_required(login_url='/login')
def blocked_user(request):
    id = request.user.id
    blocked_users = []
    user = BlockUser.objects.filter(user_id=id).first()
    profile = Profile.objects.filter(id = request.user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = id).count()

    if user:
        cursor = connection.cursor()
        query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic "\
                "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN user_blockuser s ON c.id = s.user_id " \
                "WHERE s.is_blocked= True AND s.user_id = "+ str(id);
        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(col_names, row))
            blocked_users.append(row_dict)
        context = {'user_id':id,'blocked_users':blocked_users,'profilepic': profile.profilepic,'notification_count': notification_count}
        return render(request,"blockeduser.html",context)
    context = {'user_id': id, 'blocked_users': blocked_users,'profilepic': profile.profilepic,'notification_count': notification_count}
    return render(request, "blockeduser.html", context)


@login_required(login_url='/login')
def unblocked_user(request, user_id):
    user = BlockUser.objects.filter(user_id=user_id,is_blocked = True).first()
    if user:
        if user.is_blocked == True:
            user.is_blocked = False
            user.save()
    id = request.user.id
    blocked_users = []
    cursor = connection.cursor()
    query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic " \
            "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN user_blockuser s ON c.id = s.user_id " \
            "WHERE s.is_blocked= True AND s.user_id = " + str(id);
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        blocked_users.append(row_dict)
    profile = Profile.objects.filter(id = request.user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
    context = {'user_id': id, 'blocked_users': blocked_users,'profilepic': profile.profilepic,'notification_count': notification_count}
    return render(request,"blockeduser.html",context)
