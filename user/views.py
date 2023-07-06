from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import *
from .models import *
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

# Create your views here.
def index(request):

    return render(request,"home.html")


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
def userProfile(request):
    sex = SEX_CHOICES
    context = {"sex": sex}
    return render(request, 'myprofile.html', context)
    # return render(request, 'users/user_profile.html', context)


@login_required(login_url='/login')
def edit_profile(request):
    sex = SEX_CHOICES
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        user.first_name = first_name
        user.last_name = last_name
        username = request.POST.get('username', user.username)
        user.username = username
        user.save()
        profile.avatar = request.FILES.get('avatar', profile.avatar)
        profile.placeholder = request.FILES.get('placeholder', profile.placeholder)
        profile.about = request.POST.get('about', profile.about)
        profile.sex = request.POST.get('sex', profile.sex)
        profile.is_premium = request.POST.get('is_premium', profile.is_premium)
        profile.save()
        return redirect('profile')
    context = {'user': user, 'profile': profile, "sex": sex}
    return render(request, 'editprofile.html', context)
    # return render(request, 'users/edit-profile.html', context)