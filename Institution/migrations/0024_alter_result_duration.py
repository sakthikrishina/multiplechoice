# Generated by Django 4.2.11 on 2024-05-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institution', '0023_remove_result_timestamp_result_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='duration',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
