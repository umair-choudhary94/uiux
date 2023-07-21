from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
    is_free = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    post_picture = models.ImageField(default='avatar.jpg', upload_to='post_pictures/', null=True, blank=True)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class LikeBookmarkPost(models.Model):
    id = models.AutoField(primary_key = True)
    is_bookmark = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    comment = models.TextField()
    post_id = models.IntegerField()
    user_id = models.IntegerField()

class Comments(models.Model):
    id = models.AutoField(primary_key = True)
    comment_body = models.TextField()
    user = models.IntegerField()
    post = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notifications(models.Model):
    id = models.AutoField(primary_key = True)
    notification_body = models.TextField()
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)