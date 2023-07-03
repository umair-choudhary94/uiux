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

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatar/', null=True, blank=True)
	placeholder = models.ImageField(default='avatar.jpg',upload_to='profile_placeholder/', null=True, blank=True)
	about = models.CharField(max_length=100)
	sex = models.CharField(max_length=50, choices=SEX_CHOICES, default=NONE)
	is_premium = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username


