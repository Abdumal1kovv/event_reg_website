# Generated by Django 4.1.2 on 2022-10-22 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_user_social_facebook_user_social_github_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id']},
        ),
    ]