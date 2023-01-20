# Generated by Django 4.1.2 on 2023-01-18 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pininterest', '0018_remove_follow_user_post_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='followers',
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]