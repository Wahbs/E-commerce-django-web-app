from django.contrib import admin
from Authentification.models import User
from Store.models import Produits, Photo

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'email')


admin.site.register(User, UserAdmin)


class ProduitAdmin(admin.ModelAdmin):
    list_display = ('designation', 'details_prod')


admin.site.register(Produits, ProduitAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'produit')


admin.site.register(Photo, PhotoAdmin)