from django.urls import path
from django.conf.urls import url
from . import views
# from .views import RequestPasswordResetEmail, ResetUserPassword

urlpatterns = [
    path('home/', views.index, name='home'),
    # path('profile/', views.userProfile, name='profile'),
    # path('profile/edit-profile', views.edit_profile, name='edit-profile'),
    # path('signup/', views.signup, name='signup'),
    # path('creator_register/', views.creator_signup,  name='creator_signup'),
    # path('register/', views.viewer_signup,  name='viewer_signup'),
    # path('user/login', views.user_login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('forgot_password', RequestPasswordResetEmail.as_view(), name="forgot_password"),
    # path('set-new-password/<uidb64>/<token>', ResetUserPassword.as_view(), name='reset-user-password'),
]