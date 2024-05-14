from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    def __str__(self):
        return f'{self.last_name}'

    Homme = 'Masculin'
    Femme = 'Feminin'
    Sexe_Choice = (
        (Homme, 'Masculin'),
        (Femme, 'Feminin'),
    )

    email = models.EmailField(unique=True, blank=False)
    last_name = models.CharField(max_length=30, verbose_name='Nom', blank=False)
    first_name = models.CharField(max_length=30, verbose_name='Prenom', blank=True, null=True)
    DateNaiss = models.DateField(verbose_name='Date de naissance', null=True)
    Sexe = models.CharField(max_length=10, choices=Sexe_Choice, verbose_name='Sexe', null=True)
    Photo_Profil = models.ImageField(verbose_name='Photo de profil', upload_to='Photo_profil', null=True)
    Date_created = models.DateField(verbose_name='Date creation compte', auto_now=True)
    Ville = models.CharField(max_length=30, verbose_name='Ville', blank=True, null=True)
