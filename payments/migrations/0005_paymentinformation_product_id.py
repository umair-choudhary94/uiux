# Generated by Django 3.2.16 on 2023-08-04 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentinformation',
            name='product_id',
            field=models.IntegerField(null=True),
        ),
    ]
