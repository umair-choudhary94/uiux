# Generated by Django 3.2.16 on 2023-07-12 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_subscribeblockuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribeblockuser',
            name='blocked_user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='subscribeblockuser',
            name='subscriber_id',
            field=models.IntegerField(null=True),
        ),
    ]
