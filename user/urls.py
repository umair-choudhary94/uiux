from django.urls import path
from django.conf.urls import url
from . import views
# from .views import RequestPasswordResetEmail, ResetUserPassword
from . import views
from .views import RequestPasswordResetEmail, ResetUserPassword

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.my_profile, name='profile'),
    path('editprofile', views.edit_profile, name='editprofile'),
    path('userprofile/<int:user_id>/', views.user_profile, name='userprofile'),

    path('signup/', views.signup, name='signup'),
    path('creator_register/', views.creator_signup,  name='creator_signup'),
    path('register/', views.viewer_signup,  name='viewer_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('forgot_password', RequestPasswordResetEmail.as_view(), name="forgot_password"),
    path('set-new-password/<uidb64>/<token>', ResetUserPassword.as_view(), name='reset-user-password'),
]