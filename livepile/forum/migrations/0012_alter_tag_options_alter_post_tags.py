# Generated by Django 4.1 on 2022-08-25 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_remove_reply_output'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('tag',)},
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(default=None, related_name='posts', to='forum.tag'),
        ),
    ]
