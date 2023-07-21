from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import *
from uiapp.models import *
from .forms import *
from django.contrib import messages
from django.contrib import auth
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.
@login_required(login_url='/login')
def index(request):
    sex = SEX_CHOICES
    post = []
    cursor = connection.cursor()

    query = "SELECT u.id, u.first_name, u.username, u.date_joined, pro.profilepic, po.id AS current_post_id, po.description, po.post_picture,po.created_at," \
            "lb.is_bookmark, lb.is_like, lb.post_id, lb.user_id " \
            "FROM user_user u " \
            "FULL JOIN user_profile pro ON u.id = pro.user_id " \
            "FULL JOIN user_subscribeblockuser sb ON pro.user_id = sb.user_id " \
            "FULL JOIN uiapp_post po ON pro.user_id = po.user_id " \
            "FULL JOIN uiapp_likebookmarkpost lb ON po.id = lb.post_id "\
            "ORDER BY po.id;"
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        post.append(row_dict)
    user = request.user.id
    comments = []
    cm_cursor = connection.cursor()
    cm_query = "SELECT u.id, u.first_name, u.username, u.date_joined,pro.profilepic," \
               "cm.comment_body, cm.post, cm.user " \
               "FROM user_user u " \
               "FULL JOIN user_profile pro ON u.id = pro.user_id "\
               "RIGHT JOIN uiapp_comments cm ON u.id = cm.user;"

    cm_cursor.execute(cm_query)
    cm_col_names = [col[0] for col in cm_cursor.description]
    for row in cm_cursor.fetchall():
        row_dict = dict(zip(cm_col_names, row))
        comments.append(row_dict)
    profilepic = Profile.objects.filter(id=user).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user).count()
    context = {'user_id': user, 'post': post, "comments": comments, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
    return render(request,"uiapp/home.html",context)


def signup(request):
    context = {}
    return render(request, 'signup.html', context)


def viewer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        # Validation checks
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if not any(char.isdigit() for char in password):
            errors['password'] = 'Password must contain at least one digit'
        if not any(char.isalpha() for char in password):
            errors['password'] = 'Password must contain at least one letter'
        if not any(char in '!@#$%^&*()_+-=[]{};:\'",.<>?/~`' for char in password):
            errors[
                'password'] = 'Password must contain at least one symbol, one captal letter, and at least 8 characters long'
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'

        # If there are validation errors, render the form with errors
        if errors:
            return render(request, 'normalregister.html', {'errors': errors})

        # Create new user
        try:
            # user = User.objects.create_user(username=username, email=email, password=password)
            user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.is_viewer = True
            user.save()
            # Log in user and redirect to home page
            login(request, user)
            return redirect('home')
        except IntegrityError:
            errors['username'] = 'Username already exists'
            return render(request, 'normalregister.html', {'errors': errors})
    return render(request, 'normalregister.html')


def creator_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        # Validation checks
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if not any(char.isdigit() for char in password):
            errors['password'] = 'Password must contain at least one digit'
        if not any(char.isalpha() for char in password):
            errors['password'] = 'Password must contain at least one letter'
        if not any(char in '!@#$%^&*()_+-=[]{};:\'",.<>?/~`' for char in password):
            errors[
                'password'] = 'Password must contain at least one symbol, one captal letter, and at least 8 characters long'
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'

        # If there are validation errors, render the form with errors
        if errors:
            return render(request, 'signupasseller.html', {'errors': errors})
        # Create new user
        try:
            # user = User.objects.create_user(username=username, email=email, password=password)
            user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.is_creator = True
            user.save()
            # Log in user and redirect to home page
            login(request, user)
            return redirect('home')
        except IntegrityError:
            errors['username'] = 'Username already exists'
            return render(request, 'signupasseller.html', {'errors': errors})
    return render(request, 'signupasseller.html')


def user_login(request):
    login_errors = {}
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_creator:
                    login(request, user)
                    return redirect('home')
                if user.is_viewer:
                    login(request, user)
                    return redirect('home')
                if user.is_staff:
                    login(request, user)
                    return redirect('home')

            else:
                login_errors['incorrect'] = messages.error(request, "Incorrect username or password")
                form = UserLoginForm()

    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'login_errors': login_errors, }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('login')

def terms_and_conditions(request):
    context={}
    return render(request, 'terms_and_conditions.html', context)

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, "forgot_password.html")

    def post(self, request):
        email = request.POST['email']
        context = {'values': request.POST}
        if not validate_email(email):
            messages.error(request, "Please enter a valid email")
            return render(request, "forgot_password.html", context)

        user = User.objects.filter(Q(email=email))

        if user.exists():
            for user in user:
                current_site = get_current_site(request)
                email_contents = {
                    # 'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': PasswordResetTokenGenerator().make_token(user),
                }

                link = reverse('reset-user-password', kwargs={
                    'uidb64': email_contents['uid'], 'token': email_contents['token']})

                email_subject = 'Password Reset Instructions'

                reset_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi there, please click the link below to reset your account password \n'+reset_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
            messages.success(
                request, "We have sent you an email to reset your password")
        return render(request, "forgot_password.html", context)

class ResetUserPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, "Link invalid! Please request for a new one")
                return render(request, "forgot_password.html")
        except Exception as identifier:
            pass
        return render(request, 'change_password.html', context)


@login_required(login_url='/login')
def my_profile(request):
    sex = SEX_CHOICES
    user = request.user
    profile = Profile.objects.filter(id = user.id).first()
    post = Post.objects.filter(user_id = user.id)
    comments = []
    cm_cursor = connection.cursor()
    cm_query = "SELECT u.id, u.first_name, u.username, u.date_joined,pro.profilepic," \
               "cm.comment_body, cm.post, cm.user " \
               "FROM user_user u " \
               "FULL JOIN user_profile pro ON u.id = pro.user_id "\
               "RIGHT JOIN uiapp_comments cm ON u.id = cm.user;"

    cm_cursor.execute(cm_query)
    cm_col_names = [col[0] for col in cm_cursor.description]
    for row in cm_cursor.fetchall():
        row_dict = dict(zip(cm_col_names, row))
        comments.append(row_dict)
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user':user, 'profile': profile,'post':post, "sex": sex, 'profilepic': profile.profilepic,'comments': comments,'notification_count': notification_count}
    return render(request, 'myprofile.html', context)
    # return render(request, 'users/user_profile.html', context)

@login_required(login_url='/login')
def user_profile(request,user_id):
    profile = []
    cursor = connection.cursor()
    query = "SELECT c.id, c.first_name, c.username, c.date_joined, d.profilepic,d.coverpic, d.about,d.sex, d.location,d.ethnicity,d.created_at, " \
            "s.description,s.id AS current_post_id, s.post_picture, p.is_bookmark, p.is_like,p.post_id,p.user_id "\
            "FROM user_user c LEFT JOIN user_profile d ON c.id = d.user_id LEFT JOIN uiapp_post s ON c.id = s.user_id LEFT JOIN uiapp_likebookmarkpost p "\
            "ON s.id = p.post_id WHERE c.id = " + str(user_id)
    cursor.execute(query)
    col_names = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        row_dict = dict(zip(col_names, row))
        profile.append(row_dict)
    user = User.objects.filter(id=user_id).first()
    user_profile = Profile.objects.filter(user_id = user_id).first()
    profilepic = Profile.objects.filter(id=request.user.id).first()
    comments = []
    cm_cursor = connection.cursor()
    cm_query = "SELECT u.id, u.first_name, u.username, u.date_joined,pro.profilepic," \
               "cm.comment_body, cm.post, cm.user " \
               "FROM user_user u " \
               "FULL JOIN user_profile pro ON u.id = pro.user_id "\
               "RIGHT JOIN uiapp_comments cm ON u.id = cm.user;"

    cm_cursor.execute(cm_query)
    cm_col_names = [col[0] for col in cm_cursor.description]
    for row in cm_cursor.fetchall():
        row_dict = dict(zip(cm_col_names, row))
        comments.append(row_dict)
    notification_count = Notifications.objects.filter(is_read=False, user_id = request.user.id).count()
    context = {'profile':profile, 'user':user, 'user_profile':user_profile, 'profilepic': profilepic.profilepic,'comments':comments,'notification_count': notification_count}
    return render(request, 'user_profile.html', context)
@login_required(login_url='/login')
def edit_profile(request):
    sex = SEX_CHOICES
    id = request.user.id
    user = User.objects.get(id=id)
    profile = Profile.objects.filter(user_id=id).first()
    if request.method == 'POST':
        data = request.POST
        user.first_name = data.get('name')
        user.uerusername = data.get('username')
        user.save()
        if profile:
            profile.coverpic = request.FILES.get('coverpic',profile.coverpic)
            profile.profilepic = request.FILES.get('profilepic',profile.profilepic)
            profile.about = data.get('about')
            profile.sex= data.get('sex')
            profile.location = data.get('location')
            profile.ethnicity = data.get('ethnicity')
            if data.get('is_free') == 'option1':
                if profile.is_free == True:
                    profile.is_free = False
                else:
                    profile.is_free = True
            if data.get('is_premium') == 'option2':
                if profile.is_premium == True:
                    profile.is_premium = False
                else:
                    profile.is_premium = True
            profile.save()
        else:
            profileModel = Profile()
            profileModel.coverpic = request.FILES.get('coverpic')
            profileModel.profilepic = request.FILES.get('profilepic')
            profileModel.about = data.get('about')
            profileModel.sex= data.get('sex')
            profileModel.location = data.get('location')
            profileModel.ethnicity = data.get('ethnicity')
            if data.get('is_free') == 'option1':
                profileModel.is_free = True
            if data.get('is_premium') == 'option2':
                profileModel.is_premium = True
            profileModel.user_id = id
            profileModel.save()
        profile = Profile.objects.filter(user_id=id).first()
        context = {'user': user, 'profile': profile, "sex": sex}
        return render(request, 'myprofile.html',context)
    profilepic = Profile.objects.filter(id=id).first()
    notification_count = Notifications.objects.filter(is_read=False, user_id = user.id).count()
    context = {'user': user, 'profile': profile, "sex": sex, 'profilepic': profilepic.profilepic,'notification_count': notification_count}
    return render(request, 'editprofile.html', context)
    # return render(request, 'users/edit-profile.html', context)