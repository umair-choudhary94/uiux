from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user.models import *
from django.db import connection
# Create your views here.



@login_required(login_url='/login')
def index(request):
    sex = SEX_CHOICES
    post = []
    cursor = connection.cursor()
    query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic, s.description, s.post_picture,s.created_at, p.is_bookmark, p.is_like,p.post_id,p.user_id "\
            "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN uiapp_post s ON c.id = s.user_id LEFT JOIN uiapp_likebookmarkpost p "\
            "ON s.id = p.post_id;"
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        post.append(row_dict)
    user = request.user.id
    context = {'user_id':user,'post':post, "sex": sex}
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
        query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic,d.coverpic, d.about,d.sex, d.location,d.ethnicity,d.created_at, " \
                "s.description, s.post_picture, p.is_bookmark, p.is_like,p.post_id,p.user_id " \
                "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN uiapp_post s ON c.id = s.user_id LEFT JOIN uiapp_likebookmarkpost p " \
                "ON s.id = p.post_id WHERE c.id = " + str(user.id)
        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(col_names, row))
            post.append(row_dict)
        context = {'user_id': user, 'post': post}
        return render(request,"uiapp/home.html",context)
    return render(request,"uiapp/newpost.html")

@login_required(login_url='/login')
def isbookmark(request, post_id):
    id = request.user.id
    post = LikeBookmarkPost.objects.filter(id=post_id, user_id=id).first()
    if post:
        if post.is_bookmark is True:
            post.is_bookmark = False
            post.save()
        else:
            post.is_bookmark = True
            post.save()
    else:
        postModel = LikeBookmarkPost()
        postModel.post_id = post_id
        postModel.user_id = id
        postModel.is_bookmark = True
        postModel.is_like = False
        postModel.save()
    profile = Profile.objects.filter(user_id=id)
    user = request.user
    post = Post.objects.filter()
    bookmarks = LikeBookmarkPost.objects.filter()
    context = {'user': user, 'post': post, 'profile': profile,'bookmarks':bookmarks}
    return render(request, 'uiapp/home.html', context)

@login_required(login_url='/login')
def islike(request,post_id):
    id = request.user.id
    post = LikeBookmarkPost.objects.filter(id=post_id, user_id=id).first()
    if post:
        if post.is_like =='True':
            post.is_like = False
            post.save()
        else:
            post.is_like = True
            post.save()
    else:
        postModel = LikeBookmarkPost()
        postModel.post_id = post_id
        postModel.user_id = id
        postModel.is_bookmark = False
        postModel.is_like = True
        postModel.save()
    profile = Profile.objects.filter(user_id=id)
    user = request.user
    post = Post.objects.filter(user_id=request.user.id)
    context = {'user': user, 'post': post, 'profile': profile}
    return render(request, 'uiapp/home.html', context)

@login_required(login_url='/login')
def bookmarks(request):
    sex = SEX_CHOICES
    user = User.objects.filter(id=request.user.id).first()
    profile = Profile.objects.filter(id = user.id).first()
    post = []
    cursor = connection.cursor()
    query = "SELECT c.id, c.first_name, c.username, c.date_joined, s.description, s.post_picture, p.is_bookmark, p.is_like,p.post_id,p.user_id "\
            "FROM user_user c LEFT JOIN uiapp_post s ON c.id = s.user_id LEFT JOIN uiapp_likebookmarkpost p "\
            "ON s.id = p.post_id WHERE p.is_bookmark = True AND c.id = " + str(request.user.id)
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        post.append(row_dict)
    user_id = request.user.id
    context = {'user':user, 'profile': profile,'post':post, "sex": sex, 'user_id':user_id}
    return render(request,"uiapp/bookmarks.html",context)
@login_required(login_url='/login')
def likedpost(request):
    sex = SEX_CHOICES
    user = User.objects.filter(id=request.user.id).first()
    profile = Profile.objects.filter(id = user.id).first()
    liked_posts = []
    cursor = connection.cursor()
    query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic, s.description, s.post_picture, p.is_bookmark, p.is_like,p.post_id,p.user_id "\
            "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN uiapp_post s ON c.id = s.user_id LEFT JOIN uiapp_likebookmarkpost p "\
            "ON s.id = p.post_id WHERE p.is_like = True AND c.id = " + str(request.user.id)
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        liked_posts.append(row_dict)
    context = {'user':user, 'profile': profile,'liked_posts':liked_posts, "sex": sex}
    return render(request,"uiapp/likedpost.html", context)

def notifications(request):
    return render(request,"uiapp/notifications.html")
def subscription(request):
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
    return render(request,"uiapp/subscription.html",context)


def signup(request):
    context = {}
    return render(request, 'signup.html', context)

def wallet(request):
    return render(request,"uiapp/wallet.html")

def withdraw(request):
    return render(request,"uiapp/withdraw.html")

def payment_history(request):
    return render(request,"uiapp/paymenthistory.html")

def income(request):
    return render(request,"uiapp/income.html")

def payment_information1(request):
    return render(request,"uiapp/paymentinfo1.html")

def payment_information2(request):
    return render(request,"uiapp/paymentinfo2.html")

def myprofile(request):
    return render(request,"uiapp/myprofile.html")

def edit_profile(request):
    return render(request,"uiapp/editprofile.html")
def chat(request):
    return render(request,"uiapp/chat.html")