from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
    is_free = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    post_picture = models.ImageField(default='avatar.jpg', upload_to='post_pictures/', null=True, blank=True)
    user_id = models.IntegerField()

class LikeBookmarkPost(models.Model):
    id = models.AutoField(primary_key = True)
    is_bookmark = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    comment = models.TextField()
    post_id = models.IntegerField()
    user_id = models.IntegerField()
