# Generated by Django 4.2.1 on 2023-05-31 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_blog_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='blog',
            name='last_modified',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]