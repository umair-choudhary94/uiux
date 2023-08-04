# Generated by Django 3.2.16 on 2023-08-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20230712_0649'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('blocked_user_id', models.IntegerField(null=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscribeUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_subscribed', models.BooleanField(default=False)),
                ('subscriber_id', models.IntegerField(null=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='SubscribeBlockUser',
        ),
    ]
