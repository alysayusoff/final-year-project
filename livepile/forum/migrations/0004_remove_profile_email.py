# Generated by Django 4.1 on 2022-08-22 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_delete_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]