from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.conf import settings
from Authentification.models import User
from Store.models import *
import datetime


# Create your views here.
def login_Page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour {user.username}, vous etes connectes'
                return redirect('home')
            else:
                message = 'Identififiant invalide'

    return render(request, 'Authentification/login.html', {'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


def inscription_page(request):
    form = forms.inscriptionForm()
    if request.method == 'POST':
        form = forms.inscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.inscriptionForm()

    return render(request, 'Authentification/inscription.html', {'form': form})


def upload_profile_photo(request):
    url = 'upload-photo'
    lien = 'Modifier les informations personnelles'
    if request.method == 'POST':
        form = forms.UploadProfilPhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.UploadProfilPhotoForm()
    return render(request, 'Authentification/update_profile.html', {'form': form, 'lien': lien, 'url': url})


def parametre_compte(request):
    if request.method == 'POST':
        pass
    return render(request, 'Authentification/ParametreCompte.html')


def update_profile(request):
    lien = 'Modifier photo'
    url = 'upload-profil'
    form = forms.inscriptionForm(request.POST, instance=request.user)
    if request.method == 'POST':
        if 'update_pass' in request.POST:
            form = forms.UpdatePasswordForm(request.POST, instance=request.user)
        elif 'upload_photo' in request.POST :
            form = forms.UploadProfilPhotoForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            login(request, request.user)
            return redirect('home')
    else:
        form = forms.inscriptionForm(instance=request.user)

    return render(request, 'Authentification/update_profile.html', {'form': form, 'lien': lien, 'url': url })


def update_password(request):
    url = 'update-password'
    lien = 'Modifier les informations personnelles'
    form = forms.UpdatePasswordForm(request.POST, instance=request.user)
    if request.method == 'POST':
        form = forms.UpdatePasswordForm(request.POST, instance=request.user)
        log = request.user.username
        pwd = form.cleaned_data.get('password')
        connex = authenticate(username=log, password=pwd)
        if connex is not None:
            if form.is_valid():
                form.save()
                login(request, request.user)
                return redirect('home')
        else:
            form.fields['password'].widget.attrs['class'] = 'form-control is-invalid'
            form.add_error('password', 'Le mot de passe doit etre identique a l\'ancien')

    else:
        form = forms.UpdatePasswordForm(instance=request.user)

    return render(request, 'Authentification/update_profile.html', {'form': form, 'lien': lien, 'url': url })


def profil_vendeur(request, id_vendeur):
    vendeur = get_object_or_404(User, id=id_vendeur)
    produit = Produits.objects.filter(author=vendeur)
    image = Photo.objects.filter(produit__in=produit)

    images = []
    for prod in produit:
        for i in image:
            if i.produit == prod:
                images.append(i)
                break
    mois = datetime.date.strftime(vendeur.Date_created, "%B")
    match str(mois).lower():
        case "january":
            mois = "janvier"
        case "february":
            mois = "fevrier"
        case "march":
            mois = "mars"
        case "april":
            mois = "avril"
        case "may":
            mois = "mai"
        case "june":
            mois = "juin"
        case "july":
            mois = "juillet"
        case "august":
            mois = "aout"
        case "september":
            mois = "septembre"
        case "october":
            mois = "octobre"
        case "november":
            mois = "novembre"
        case "december":
            mois = "decembre"

    date_rejoint = datetime.date.strftime(vendeur.Date_created, "{} %Y".format(mois))
    context = {
        'vendeur': vendeur,
        'produit': produit,
        'images': images,
        'date_rejoint': date_rejoint,
    }
    return render(request, 'Authentification/profil_vendeur.html', context)