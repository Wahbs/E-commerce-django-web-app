# Generated by Django 4.1.6 on 2023-02-13 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_remove_photo_fichier_images_photo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='produits',
            name='vendu',
            field=models.BooleanField(default=False),
        ),
    ]
