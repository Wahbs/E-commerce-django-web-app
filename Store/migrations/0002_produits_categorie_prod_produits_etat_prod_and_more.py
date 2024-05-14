# Generated by Django 4.1.6 on 2023-02-08 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produits',
            name='categorie_prod',
            field=models.CharField(choices=[('Appareils electro-menager', 'Appareils electro-menager'), ('Accessoires', 'Accessoires'), ('Telephone portable', 'Telephone portable'), ('Auto-mobile', 'Auto-mobile'), ('Autres', 'Autres')], default='Autres', max_length=50, verbose_name='Catégorie'),
        ),
        migrations.AddField(
            model_name='produits',
            name='etat_prod',
            field=models.CharField(choices=[('Neuf', 'Neuf'), ("D'occasion comme neuf", "D'occasion comme neuf"), ('Occasion', 'Occasion')], default='Occasion', max_length=50, verbose_name='Etat du produit'),
        ),
        migrations.AddField(
            model_name='produits',
            name='prix_prod',
            field=models.PositiveIntegerField(default=0, verbose_name='Prix du produit'),
        ),
        migrations.AddField(
            model_name='produits',
            name='promotion_prod',
            field=models.CharField(choices=[('Oui', 'Oui'), ('Non', 'Non')], default='Non', max_length=5, verbose_name='Mise en promotion ?'),
        ),
        migrations.AddField(
            model_name='produits',
            name='ville_prod',
            field=models.CharField(default='Autres', max_length=15, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='produits',
            name='designation',
            field=models.CharField(max_length=128, verbose_name='Désignation'),
        ),
        migrations.AlterField(
            model_name='produits',
            name='details_prod',
            field=models.CharField(max_length=1000, verbose_name='Détails du produit'),
        ),
    ]