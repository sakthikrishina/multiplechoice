# Generated by Django 4.2.11 on 2024-04-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customuser_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_profile',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pic/%Y/%m/%d/'),
        ),
    ]
