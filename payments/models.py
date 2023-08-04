from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=500)
    product_desc = models.TextField()
    product_price = models.IntegerField()
    currency = models.CharField(max_length=100)
    user_id = models.IntegerField(null=True)

class PaymentInformation(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=300)
    card_information = models.IntegerField()
    card_date = models.CharField(max_length=5)
    card_cvc = models.IntegerField()
    card_owner_name = models.CharField(max_length=500)
    country = models.CharField(max_length=300)
    address = models.CharField(max_length=600)
    user_id = models.IntegerField(null=True)
    product_id = models.IntegerField(null=True)

class SubscribeUser(models.Model):
    id = models.AutoField(primary_key = True)
    is_subscribed = models.BooleanField(default=False)
    creator_id = models.IntegerField(null=True)
    subscriber_id = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(auto_now_add=False, null=True)

class TransactionInformation(models.Model):
    id = models.AutoField(primary_key=True)
    card_owner_id = models.IntegerField()
