# Generated by Django 4.1.6 on 2023-02-09 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_alter_photo_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='post_id',
            new_name='produit',
        ),
    ]
