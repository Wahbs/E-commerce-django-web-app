# Generated by Django 4.1.6 on 2023-03-07 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Discussion', '0004_rename_fichier_message_chatmessages_fichier_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessages',
            name='statut',
            field=models.BooleanField(default=False, verbose_name='Message lu'),
        ),
    ]
