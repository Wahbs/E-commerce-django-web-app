import datetime

from django.db import models
from django.conf import settings
from PIL import Image


class Produits(models.Model):
    def __str__(self):
        return f'{self.designation}'

    Categorie_Choice = [
        ('Appareils electro-menager', 'Appareils electro-menager'), ('Accessoires', 'Accessoires'),
        ('Telephone portable', 'Telephone portable'), ('Auto-mobile', 'Auto-mobile'), ('Autres', 'Autres'),
    ]
    Etat_Choice = [
        ('Neuf', 'Neuf'), ('D\'occasion comme neuf', 'D\'occasion comme neuf'), ('Occasion', 'Occasion'),
    ]
    Ville_Choice = [
        ('Bafoussam', 'Bafoussam'), ('Bamenda', 'Bamenda'), ('Bertoua', 'Bertoua'), ('Buea', 'Buea'),
        ('Douala', 'Douala'), ('Ebolowa', 'Ebolowa'), ('Garoua', 'Garoua'), ('Maroua', 'Maroua'),
        ('Ngaoundere','Ngaoundere'), ('Yaounde', 'Yaounde'), ('Autres', 'Autres')
    ]
    Est_promotion =[
        ('Oui', 'Oui'), ('Non', 'Non')
    ]
    designation = models.CharField(max_length=128, verbose_name='Désignation')
    categorie_prod = models.CharField(max_length=50, choices=Categorie_Choice, verbose_name='Catégorie', blank=False, default='')
    etat_prod = models.CharField(max_length=50, choices=Etat_Choice, verbose_name='Etat du produit', blank=False, default='Occasion')
    details_prod = models.CharField(max_length=1000, verbose_name='Détails du produit', )
    ville_prod = models.CharField(max_length=15, verbose_name='Ville', choices=Ville_Choice, default='Autres')
    prix_prod = models.PositiveIntegerField(verbose_name='Prix du produit', default=0)
    prix_promo = models.PositiveIntegerField(verbose_name='Prix promotionnel', default=0)
    promotion_prod = models.CharField(max_length=5, verbose_name='Mise en promotion ?', choices=Est_promotion, default='Non')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, )
    starred = models.BooleanField(default=False)
    word_count = models.IntegerField(null=True)
    vendu = models.BooleanField(default=False)

    def _get_word_count(self):
        word = str(self.details_prod)
        count = len(word)
        return count

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.word_count = self._get_word_count()


# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to='Image_Produit', blank=True)
    titre = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    produit = models.ForeignKey(Produits, null=False, on_delete=models.CASCADE)
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
            # sauvegarde de l’image redimensionnée dans le système de fichiers
            # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Panier(models.Model):
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE, null=False)
    Acheteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='acheteur_set')
    Vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='vendeur_set')
    date_ajout = models.DateTimeField(verbose_name='Date d\'ajout', auto_now=True)