# Generated by Django 4.2.11 on 2024-04-14 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_alter_customuser_options_customuser_mpin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='382171', max_length=6),
        ),
    ]
