# Generated by Django 4.1.7 on 2023-03-29 11:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='social',
        ),
        migrations.AddField(
            model_name='social',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='socials', to=settings.AUTH_USER_MODEL),
        ),
    ]
