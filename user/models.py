from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
import uuid
from django.conf import settings
from .constants import SEX_CHOICES
from .constants import NONE

# Create your models here.

class User(AbstractUser):
	is_creator=models.BooleanField(default=False)
	is_viewer=models.BooleanField(default=False)
	is_subscribed=models.BooleanField(default=False)

class Profile(models.Model):
	id = models.AutoField(primary_key=True)
	profilepic = models.ImageField(default='avatar.jpg', upload_to='profile_avatar/', null=True, blank=True)
	coverpic = models.ImageField(default='avatar.jpg',upload_to='profile_placeholder/', null=True, blank=True)
	about = models.CharField(max_length=100)
	sex = models.CharField(max_length=50, choices=SEX_CHOICES, default=NONE)
	location = models.CharField(max_length=300, null=True)
	ethnicity = models.CharField(max_length=300, null=True)
	is_free = models.BooleanField(default=False)
	is_premium = models.BooleanField(default=False)
	user_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

class SubscribeBlockUser(models.Model):
	id = models.AutoField(primary_key = True)
	is_subscribed = models.BooleanField(default=False)
	is_blocked = models.BooleanField(default=False)
	subscriber_id = models.IntegerField(null=True)
	blocked_user_id = models.IntegerField(null=True)
	user_id = models.IntegerField()