import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from Store import models, forms
from Authentification.models import User
from django.db.models import Q
from Store.models import Panier, Produits, Photo
from Discussion.models import chatMessages
# Create your views here.


def home_Page(request):
    nb_message = 0
    recherche = 0
    if request.user.is_authenticated:
        nb_panier = Panier.objects.filter(Acheteur_id=request.user.id).count()
        nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    else:
        nb_panier = 0
    if Produits.objects.all().exists():
        if request.method == 'GET':
            if 'q' in request.GET and request.GET['q'].strip():
                recherche = request.GET['q']
                produits = Produits.objects.filter(designation__icontains=recherche)

                if len(produits) == 0:
                    return render(request, 'index.html', {'recherche': recherche, 'nb_panier': nb_panier, 'nb_message': nb_message})

        produits = Produits.objects.all()

        if Photo.objects.filter(produit_id__in=produits).exists():
            photos = Photo.objects.filter(produit_id__in=produits)
            images = []
            for produit in produits:
                for image in photos:
                    if image.produit == produit:
                        images.append(image)
                        break

        else:
            photos = None
        recherche = 0
        return render(request, 'index.html', {'produits': produits, 'photos': photos, 'images': images,
                                              'nb_panier': nb_panier, 'nb_message': nb_message, 'recherche': recherche})
    else:
        produits = None
        photos = None
        recherche = 0
    return render(request, 'index.html', {'produits': produits, 'photos': photos, 'nb_panier': nb_panier,
                                          'recherche': recherche, 'nb_message': nb_message})


@login_required
def creation_produit(request):
    produit_form = forms.ajout_produitFrom()
    nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    photo_form = forms.photo_produitsForm()
    if request.method == 'POST':
        produit_form = forms.ajout_produitFrom(request.POST)
        photo_form = forms.photo_produitsForm(request.POST, request.FILES)
        images = request.FILES.getlist('photo')
        if len(images) == 0:
            photo_form.fields['photo'].widget.attrs['class'] = 'form-control is-invalid'
        if produit_form.is_valid() and len(images) != 0:
            produit = produit_form.save(commit=False)
            produit.author = request.user
            produit.save()

            for image in images:
                Photo.objects.create(image=image, titre=produit.designation, uploader=request.user, produit=produit)

                # photo = photo_form.save(commit=False)
                # photo.post_id = produit
                # photo.uploader = request.user
                # photo.save()
            return redirect('home')
    return render(request, 'Store/creer_produit.html', {'produit_form': produit_form, 'photo_form': photo_form, 'nb_message': nb_message })


@login_required
def mes_produits(request):
    nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    if Produits.objects.filter(author_id=request.user).exists():
        produits = Produits.objects.filter(author_id=request.user)
        if Photo.objects.filter(produit_id__in=produits).exists():
            photos = Photo.objects.filter(produit_id__in=produits)
            images = []
            for produit in produits:
                for image in photos:
                    if image.produit == produit:
                        images.append(image)
                        break

        else:
            photos = None

        return render(request, 'Store/mes_produits.html', {'produits': produits, 'photos': photos, 'images': images })
    else:
        produits = None
        photos = None

        return render(request, 'Store/mes_produits_Empty.html', {'produits': produits, 'photos': photos, 'nb_message': nb_message})


@login_required
def ajout_produit(request):
    nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    form = forms.ajout_produitFrom()
    if request.method == 'POST':
        form = forms.ajout_produitFrom(request.POST)
        if form.is_valid():
            # form.save()
            return redirect('home')
    else:
        form = forms.ajout_produitFrom()
    return render(request, 'Store/mes-produits.html', {'nb_message': nb_message})


@login_required
def details_produits(request, IDproduit):
    nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    produit = get_object_or_404(models.Produits, id=IDproduit)
    produits = models.Photo.objects.filter(produit_id=produit)
    photo_form = forms.photo_produitsForm()
    if request.method == 'POST':
        images = request.FILES.getlist('photo')
        if len(images) == 0:
            pass
        else:
            for image in images:
                models.Photo.objects.create(image=image, titre=produit.designation, uploader=request.user, produit=produit)

            return redirect('detail-produit', produit.id)

    return render(request, 'Store/detail_produit.html', {'images': produits, 'produit': produit, 'photo_form': photo_form, 'nb_message': nb_message})


def details_produit_vente(request, IDproduit):
    produit = get_object_or_404(models.Produits, id=IDproduit)
    produits = models.Photo.objects.filter(produit_id=produit)
    nb_message = 0
    discussion = 0
    prod = []
    if request.user.is_authenticated:
        nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
        discussion = chatMessages.objects.filter(user_to=produit.author, user_from=request.user, produit=produit).count()
        paniers = Panier.objects.filter(Acheteur_id=request.user)
        for pan in paniers:
            prod.append(pan.produit)
        if produit in prod:
            lien = 'supprime-prod-panier'
            panier = 1
        else:
            lien = 'ajout-panier'
            panier = 0
    else:
        paniers = None
        lien = 'ajout-panier'
        panier = 0

    context = {
        'images': produits,
        'produit': produit,
        'panier': panier,
        'lien': lien,
        'nb_message': nb_message,
        'discussion': discussion,
    }
    return render(request, 'Store/detail_produit_vente.html', context)


@login_required
def modifier_produit(request, IDproduit):
    nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    produit = get_object_or_404(models.Produits, id=IDproduit)
    produit_form = forms.ajout_produitFrom(instance=produit)

    if request.method == 'POST':
        produit_form = forms.ajout_produitFrom(request.POST, instance=produit)
        if produit_form.is_valid():
            produit = produit_form.save(commit=False)
            produit.save()

            return redirect('detail-produit', produit.id)
    return render(request, 'Store/modifier-produit.html', {'produit_form': produit_form, 'produit': produit, 'nb_message': nb_message})


@login_required
def delete_image(request, IDimage):
    image = get_object_or_404(models.Photo, id=IDimage)
    produit = get_object_or_404(models.Produits, id=image.produit_id)
    images = models.Photo.objects.filter(produit_id=produit)

    image.delete()
    return redirect('detail-produit', produit.id)

    # return render(request, 'Store/detail_produit.html', {'images': images, 'produit': produit})


@login_required
def vendu_produit(request, IDproduit):
    produit = get_object_or_404(Produits, id=IDproduit)

    produit.vendu = True
    produit.save()

    return redirect('detail-produit', produit.id)


@login_required
def annule_produit_vendu(request, IDproduit):
    produit = get_object_or_404(Produits, id=IDproduit)

    produit.vendu = False
    produit.save()

    return redirect('detail-produit', produit.id)


@login_required
def supprimer_produit(request, IDproduit):
    produit = get_object_or_404(models.Produits, id=IDproduit)

    produit.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def ajout_panier(request, IDproduit):
    produit = get_object_or_404(Produits, id=IDproduit)
    panier = Panier.objects.filter(Acheteur_id=request.user)
    vendeur = produit.author

    produits = []
    for pan in panier:
        produits.append(pan.produit)
    if produit in produits:
        pass
    else:
        Panier.objects.create(Acheteur=request.user, Vendeur=vendeur, produit=produit, date_ajout=datetime.date.today)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def mon_panier(request):
    nb_message = chatMessages.objects.filter(Q(user_to=request.user.id, statut=False)).count()
    panier = Panier.objects.filter(Acheteur_id=request.user)
    nb_panier = Panier.objects.filter(Acheteur_id=request.user.id).count()
    produits = []
    for produit in panier:
        produits.append(produit.produit)
    if Photo.objects.filter(produit_id__in=produits).exists():
        photos = Photo.objects.filter(produit_id__in=produits)
        images = []
        for produit in produits:
            for image in photos:
                if image.produit == produit:
                    images.append(image)
                    break
        return render(request, 'Store/mon_panier.html', {'panier': panier, 'nb_panier': nb_panier, 'images': images, 'nb_message': nb_message})

    else:
        photos = None

    return render(request, 'Store/mon_panier.html', {'panier': panier, 'nb_panier': nb_panier, 'nb_message': nb_message})


@login_required
def supprimer_prod_panier(request, IDproduit):
    panier = Panier.objects.filter(Acheteur_id=request.user)
    produit = get_object_or_404(models.Produits, id=IDproduit)
    for prod in panier:
        if prod.produit == produit:
            prod.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('mon-panier')