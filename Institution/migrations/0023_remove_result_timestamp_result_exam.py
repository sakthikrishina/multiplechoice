# Generated by Django 4.2.11 on 2024-05-09 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Institution', '0022_remove_result_exam_result_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='result',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institution.course'),
        ),
    ]
