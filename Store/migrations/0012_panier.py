# Generated by Django 4.1.6 on 2023-02-15 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Store', '0011_produits_prix_promo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ajout', models.DateTimeField(auto_now=True, verbose_name="Date d'ajout")),
                ('Acheteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acheteur_set', to=settings.AUTH_USER_MODEL)),
                ('Vendeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendeur_set', to=settings.AUTH_USER_MODEL)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.produits')),
            ],
        ),
    ]