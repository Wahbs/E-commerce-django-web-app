"""MobileStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import Store.views
import Discussion.views
import Authentification.views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Store.views.home_Page, name='home'),
    path('login/', Authentification.views.login_Page, name='login'),
    path('logout/', Authentification.views.logout_user, name='log-out'),
    path('inscription/', Authentification.views.inscription_page, name='inscription'),
    path('upload/Photo_Profil', Authentification.views.upload_profile_photo, name='upload-photo'),
    path('parametre/', Authentification.views.parametre_compte, name='parametre'),
    path('update/profile', Authentification.views.update_profile, name='update-profile'),
    path('update/password', Authentification.views.update_password, name='update-password'),
    path('profil/utilisateur/<int:id_vendeur>/', Authentification.views.profil_vendeur, name='profil-vendeur'),

    path('creer-produit/', Store.views.creation_produit, name='creer-produit'),
    path('Mes-produits/', Store.views.mes_produits, name='mes-produits'),
    path('Details-produit/<int:IDproduit>/', Store.views.details_produits, name='detail-produit'),
    path('Details-produit-vente/<int:IDproduit>/', Store.views.details_produit_vente, name='detail-produit-vente'),
    path('Modifier-produit/<int:IDproduit>/', Store.views.modifier_produit, name='modifier-produit'),
    path('Delete-image/<int:IDimage>/', Store.views.delete_image, name='delete-image'),
    path('marquer-vendu/<int:IDproduit>/', Store.views.vendu_produit, name='vendu-produit'),
    path('annule-vente/<int:IDproduit>/', Store.views.annule_produit_vendu, name='annule-produit-vendu'),
    path('supprimer-produit/<int:IDproduit>/', Store.views.supprimer_produit, name='supprimer-produit'),
    path('ajout-panier/<int:IDproduit>/', Store.views.ajout_panier, name='ajout-panier'),
    path('mon-panier/', Store.views.mon_panier, name='mon-panier'),
    path('supprimer-du-panier/<int:IDproduit>/', Store.views.supprimer_prod_panier, name='supprime-prod-panier'),

    path('discussion/', Discussion.views.home_chat, name='home-chat'),
    path('actualise_chat/<int:chat_id>/<int:prod_id>/', Discussion.views.actualise_chat, name='actualise_chat'),
    path('actualise_discussion/<int:chat_id>/<int:prod_id>/', Discussion.views.actualise_list_discussion, name='actualise_discussion'),
    path('send/', Discussion.views.send_chat, name='chat-send'),
    path('supprime_msg/<int:msg_id>/', Discussion.views.supprime_chat, name='supprime-msg'),
]
urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
