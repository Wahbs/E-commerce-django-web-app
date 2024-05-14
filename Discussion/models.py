from django.db import models
from django.conf import settings
from django.utils import timezone
from Store.models import *
# Create your models here.


class chatMessages(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    message = models.TextField()
    statut = models.BooleanField(verbose_name="Message lu", default=False)
    fichier_message = models.FileField(upload_to="Message_fichier", blank=True)
    produit = models.ForeignKey(Produits, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


class Inbox(models.Model):
    acheteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    produit = models.ForeignKey(Produits, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=timezone.now)