from django.db import models

# Create your models here.
class PaymentInformation(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=300)
    card_information = models.IntegerField()
    card_date = models.DateTimeField()
    card_cvc = models.IntegerField()
    card_owner_name = models.CharField(max_length=500)
    country = models.CharField(max_length=300)
    address = models.CharField(max_length=600)
    user_id = models.IntegerField(null=True)

class TransactionInformation(models.Model):
    id = models.AutoField(primary_key=True)
    card_owner_id = models.IntegerField()
