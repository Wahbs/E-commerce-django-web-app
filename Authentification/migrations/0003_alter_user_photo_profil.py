# Generated by Django 4.1.6 on 2023-02-08 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentification', '0002_alter_user_photo_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Photo_Profil',
            field=models.ImageField(upload_to='', verbose_name='Photo de profil'),
        ),
    ]