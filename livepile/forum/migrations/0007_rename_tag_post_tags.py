# Generated by Django 4.1 on 2022-08-23 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_rename_tags_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tag',
            new_name='tags',
        ),
    ]
