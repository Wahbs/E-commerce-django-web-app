# Generated by Django 4.1.6 on 2023-02-08 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Produits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=128)),
                ('details_prod', models.CharField(max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('starred', models.BooleanField(default=False)),
                ('word_count', models.IntegerField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('titre', models.CharField(blank=True, max_length=128)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Store.produits')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
