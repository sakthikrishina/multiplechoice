# Generated by Django 4.2.11 on 2024-04-14 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]