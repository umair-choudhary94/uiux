from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import *
from payments.models import *
from django.db import connection
# Create your views here.



@login_required(login_url='/login')
def index(request):
    sex = SEX_CHOICES
    post = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined,u.is_creator, pro.profilepic, po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
            "lb.is_bookmark, lk.is_like, lb.post_id, lb.user_id " \
            "FROM user_user u " \
            "FULL JOIN user_profile pro ON u.id = pro.user_id " \
            "FULL JOIN uiapp_post po ON pro.user_id = po.user_id " \
            "LEFT JOIN uiapp_bookmarkpost lb ON po.id = lb.post_id FULL JOIN uiapp_likepost lk ON po.id = lk.post_id " \
            "ORDER BY po.id;"
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        post.append(row_dict)
    user = request.user
    comments = []
    cm_cursor = connection.cursor()
    cm_query = "SELECT u.id, u.first_name, u.username, u.date_joined,pro.profilepic," \
               "cm.comment_body, cm.post, cm.user " \
               "FROM user_user u " \
               "FULL JOIN user_profile pro ON u.id = pro.user_id " \
               "RIGHT JOIN uiapp_comments cm ON u.id = cm.user;"
    cm_cursor.execute(cm_query)
    cm_col_names = [col[0] for col in cm_cursor.description]
    for row in cm_cursor.fetchall():
        row_dict = dict(zip(cm_col_names, row))
        comments.append(row_dict)
    profilepic = Profile.objects.filter(id=user.id).first()
    notification_count = Notifications.objects.filter(is_read = False, user_id = user.id).count()
    context = {'user_id': user.id,'user':user, 'post': post, "comments": comments, 'profilepic': profilepic.profilepic,'notification_count':notification_count}
    return render(request,"uiapp/home.html",context)

@login_required(login_url='/login')
def new_post(request):
    user = User.objects.filter(id=request.user.id).first()
    if request.method == 'POST':
        post = Post()
        data = request.POST
        post.description = data.get('description')
        post.is_free = 'True'
        post.is_premium = 'False'
        post.post_picture = request.FILES.get('post_picture')
        post.user_id = user.id
        post.save()
        post = []
        cursor = connection.cursor()
        query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic,po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
                "lb.is_bookmark, lb.is_like, lb.post_id, lb.user_id " \
                "FROM user_user u " \
                "INNER JOIN user_profile pro ON u.id = pro.user_id " \
                "INNER JOIN uiapp_post po ON pro.user_id = po.user_id " \
                "INNER JOIN uiapp_likebookmarkpost lb ON po.user_id = lb.user_id WHERE u.id = " + str(user.id)
        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(col_names, row))
            post.append(row_dict)
        profilepic = Profile.objects.filter(id=user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
        context = {'user_id': user,'user':request.user, 'post': post, 'profilepic': profilepic.profilepic,'notification_count':notification_count}
        return render(request,"uiapp/home.html",context)
    return render(request,"uiapp/newpost.html")

@login_required(login_url='/login')
def isbookmark(request):
    current_post_id = request.POST.get('post_id')
    id = request.user.id
    post = BookmarkPost.objects.filter(post_id=current_post_id, user_id=id).first()
    if post:
        if post.is_bookmark is True:
            post.is_bookmark = False
            post.save()
        else:
            post.is_bookmark = True
            post.save()
            notificationModel = Notifications()
            notificationModel.notification_body = str(request.user.username) + "has liked your post."
            notificationModel.user_id = id
            notificationModel.post_id = current_post_id
            notificationModel.save()
    else:
        postModel = BookmarkPost()
        postModel.post_id = current_post_id
        postModel.user_id = id
        postModel.is_bookmark = True
        postModel.save()

    post = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic, po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
            "lb.is_bookmark, lb.post_id, lb.user_id " \
            "FROM user_user u " \
            "FULL JOIN user_profile pro ON u.id = pro.user_id " \
            "FULL JOIN uiapp_post po ON pro.user_id = po.user_id " \
            "FULL JOIN uiapp_bookmarkpost lb ON po.id = lb.post_id "\
            "ORDER BY po.id;"
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        post.append(row_dict)
    user = request.user.id
    profilepic = Profile.objects.filter(id=user).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user).count()
    context = {'user_id':user,'user':request.user,'post':post, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
    return render(request, 'uiapp/home.html', context)

@login_required(login_url='/login')
def islike(request):
    current_post_id = request.POST.get('post_id')
    print(current_post_id)
    id = request.user.id
    post = LikePost.objects.filter(post_id=current_post_id, user_id=id).first()
    if post:
        if post.is_like is True:
            post.is_like = False
            post.save()
        else:
            post.is_like = True
            post.save()
            notificationModel = Notifications()
            notificationModel.notification_body = str(request.user.username) + "has liked your post."
            notificationModel.user_id = id
            notificationModel.post_id = current_post_id
            notificationModel.save()
    else:
        postModel = LikePost()
        postModel.post_id = current_post_id
        postModel.user_id = id
        postModel.is_like = True
        postModel.save()
        notificationModel = Notifications()
        notificationModel.notification_body = str(request.user.username) + "has liked your post."
        notificationModel.user_id = id
        notificationModel.post_id = current_post_id
        notificationModel.save()
    profile = Profile.objects.filter(user_id=id)
    user = request.user
    post = Post.objects.filter(user_id=request.user.id)
    profilepic = Profile.objects.filter(id=user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user': user, 'post': post, 'profile': profile, 'profilepic':profilepic.profilepic,'notification_count': notification_count}
    return render(request, 'uiapp/home.html', context)

@login_required(login_url='/login')
def bookmarks(request):
    sex = SEX_CHOICES
    user = User.objects.filter(id=request.user.id).first()
    profile = Profile.objects.filter(id = user.id).first()
    post = []
    cursor = connection.cursor()
    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic,po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
            "lb.is_bookmark, lb.post_id, lb.user_id " \
            "FROM user_user u " \
            "INNER JOIN user_profile pro ON u.id = pro.user_id " \
            "INNER JOIN uiapp_post po ON pro.user_id = po.user_id " \
            "INNER JOIN uiapp_bookmarkpost lb ON po.id = lb.post_id WHERE lb.is_bookmark ='1' AND lb.user_id = " + str(user.id)
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        post.append(row_dict)
    user_id = request.user.id
    profilepic = Profile.objects.filter(id=user_id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user':user, 'profile': profile,'post':post, "sex": sex, 'user_id':user_id, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
    return render(request,"uiapp/bookmarks.html",context)
@login_required(login_url='/login')
def likedpost(request):
    sex = SEX_CHOICES
    user = User.objects.filter(id=request.user.id).first()
    profile = Profile.objects.filter(id = user.id).first()
    liked_posts = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic,po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
            "lb.is_like, lb.post_id, lb.user_id " \
            "FROM user_user u " \
            "INNER JOIN user_profile pro ON u.id = pro.user_id " \
            "INNER JOIN uiapp_post po ON pro.user_id = po.user_id " \
            "INNER JOIN uiapp_likepost lb ON po.id = lb.post_id WHERE lb.is_like ='1' AND lb.user_id = " + str(user.id)

    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        liked_posts.append(row_dict)
    profilepic = Profile.objects.filter(id=user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user':user, 'profile': profile,'liked_posts':liked_posts, "sex": sex, 'user_id':user.id, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
    return render(request,"uiapp/likedpost.html", context)

@login_required(login_url='/login')
def comments(request):
    current_post_id = request.POST.get('post_id')
    if request.method == 'POST':
        data = request.POST
        commentModel = Comments()
        commentModel.comment_body = data.get('comment_body')
        commentModel.user = request.user.id
        commentModel.post = data.get('post_id')
        commentModel.save()
        notificationModel = Notifications()
        notificationModel.notification_body = str(request.user.username) + "has commented on your post."
        notificationModel.user_id = request.user.id
        notificationModel.post_id = current_post_id
        notificationModel.save()
        sex = SEX_CHOICES
        post = []
        cursor = connection.cursor()

        query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic, po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
                "lb.is_bookmark, lb.is_like, lb.post_id, po.user_id " \
                "FROM user_user u " \
                "INNER JOIN user_profile pro ON u.id = pro.user_id " \
                "INNER JOIN uiapp_post po ON pro.user_id = po.user_id " \
                "INNER JOIN uiapp_bookmarkpost lb ON po.id = lb.post_id " \
                "ORDER BY po.id;"
        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(col_names, row))
            post.append(row_dict)
        user_id = request.user.id

        comments = []
        cm_cursor = connection.cursor()
        cm_query = "SELECT u.id, u.first_name, u.username, u.date_joined,pro.profilepic," \
                   "cm.comment_body, cm.post, cm.user " \
                   "FROM user_user u " \
                   "FULL JOIN user_profile pro ON u.id = pro.user_id " \
                   "RIGHT JOIN uiapp_comments cm ON u.id = cm.user;"
        cm_cursor.execute(cm_query)
        cm_col_names = [col[0] for col in cm_cursor.description]
        for row in cm_cursor.fetchall():
            row_dict = dict(zip(cm_col_names, row))
            comments.append(row_dict)
        profilepic = Profile.objects.filter(id=user_id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id = user_id).count()
        context = {'user_id': user_id,'user':request.user,'post': post, "comments": comments,'profilepic': profilepic.profilepic, 'notification_count': notification_count}
        return render(request,"uiapp/home.html",context)
def notifications(request):
    sex = SEX_CHOICES
    user = User.objects.filter(id=request.user.id).first()
    profile = Profile.objects.filter(id = user.id).first()
    notifications = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic," \
            "nt.notification_body,nt.id AS notification_id, nt.user_id, nt.post_id " \
            "FROM user_user u " \
            "FULL JOIN user_profile pro ON u.id = pro.user_id " \
            "RIGHT JOIN uiapp_notifications nt ON u.id = nt.user_id WHERE nt.is_read ='0' AND u.id = " + str(user.id)

    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        notifications.append(row_dict)
    profilepic = Profile.objects.filter(id=user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user':user, 'profile': profile,'notifications':notifications, "sex": sex, 'user_id':user.id, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
    return render(request,"uiapp/notifications.html",context)

def read_notification(request):
    if request.method == 'POST':
        id =  request.POST.get('notification_id')
        notifcation = Notifications.objects.filter(id=id).first()
        if notifcation is not None:
            notifcation.is_read = True
            notifcation.save()
        sex = SEX_CHOICES
        user = User.objects.filter(id=request.user.id).first()
        profile = Profile.objects.filter(id=user.id).first()
        notifications = []
        cursor = connection.cursor()

        query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic," \
                "nt.notification_body,nt.id AS notification_id, nt.user_id, nt.post_id " \
                "FROM user_user u " \
                "FULL JOIN user_profile pro ON u.id = pro.user_id " \
                "RIGHT JOIN uiapp_notifications nt ON u.id = nt.user_id WHERE nt.is_read ='0' AND u.id = " + str(
            user.id)

        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(col_names, row))
            notifications.append(row_dict)
        profilepic = Profile.objects.filter(id=user.id).first()
        notification_count = Notifications.objects.filter(is_read=False, user_id=user.id).count()
        context = {'user': user, 'profile': profile, 'notifications': notifications, "sex": sex, 'user_id': user.id,
                   'profilepic': profilepic.profilepic, 'notification_count': notification_count}
        return render(request, "uiapp/notifications.html", context)

def signup(request):
    context = {}
    return render(request, 'signup.html', context)

def account_detail(request):
    profilepic = Profile.objects.filter(id=request.user.id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id=request.user.id).count()
    accountDetail = PaymentInformation.objects.filter(user_id=request.user.id).first()
    context = {'user': request.user, 'user_id': request.user.id, 'accountDetail': accountDetail,
               'profilepic': profilepic.profilepic, 'notification_count': notification_count}
    return render(request, 'uiapp/accountdetail.html', context)
def myprofile(request):
    return render(request,"uiapp/myprofile.html")

def edit_profile(request):
    return render(request,"uiapp/editprofile.html")
