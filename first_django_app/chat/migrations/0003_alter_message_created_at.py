# Generated by Django 4.2.6 on 2023-10-14 12:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
