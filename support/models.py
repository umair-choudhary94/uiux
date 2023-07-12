from django.db import models

# Create your models here.

class CustormerSupport(models.Model):
    id = models.AutoField(primary_key = True)
    question = models.TextField()
    answer = models.TextField()
    user_id = models.IntegerField()


