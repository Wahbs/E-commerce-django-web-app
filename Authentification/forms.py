from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import datetime
from Authentification.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
                               max_length=60, label='Nom d\'utilisateur')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Mot de passe'}),
                               max_length=60, label='Mot de passe')


class inscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'Sexe', 'DateNaiss', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Prenom', },),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemple@gmail.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
            'DateNaiss': forms.DateInput(attrs={'type': 'date'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Mot de passe'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirmer mot de passe',})
        }

    def __init__(self, *args, **kwargs):
        super(inscriptionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if self.errors:
                if visible.errors:
                    visible.field.widget.attrs['class'] = 'form-control is-invalid'
                else:
                    visible.field.widget.attrs['class'] = 'form-control is-valid'

            visible.field.widget.attrs['id'] = 'floatingInput'

    def clean(self):
        super(inscriptionForm, self).clean()
        # Recuperation des champs du formulaire
        nom = self.cleaned_data.get('last_name')
        prenom = self.cleaned_data.get('first_name')
        user = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        date = self.cleaned_data.get('DateNaiss')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # Gestion des erreurs

        if nom:
            if len(nom) < 3:
                self.add_error('last_name', 'Taille du nom incorrect (au moins 3 lettres)')

            if not any(character.isalpha for character in nom):
                self.add_error('nom', 'Le nom entré est incorrect')

        if prenom:
            if len(prenom) < 2:
                self.add_error('last_name', 'Taille du prenom incorrect (au moins 2 lettres)')
            if not any(character.isalpha for character in prenom):
                self.add_error('prenom', 'Le prenom entré est incorrect')

        if user:
            if len(user) < 3:
                self.add_error('last_name', 'Taille du nom d\'utilisateur incorrect (au moins 3 lettres)')

        if password1:
            if not any(character.isdigit() for character in password1):
                self.add_error('password1', 'Le mot de passe doit contenir au moins un chiffre')

            if len(password1) < 6:
                self.add_error('password1', 'Le mot de passe doit avoir au moins 6 caracteres')

        if date:
            if date.year > (datetime.date.today().year - 10):
                self.add_error('DateNaiss', 'Vous devez avoir au moins 10ans')

        return self.cleaned_data


class UploadProfilPhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('Photo_Profil', )

    def __init__(self, *args, **kwargs):
        super(UploadProfilPhotoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['id'] = 'Image'
            visible.field.widget.attrs['class'] = 'uploadFile img'
            visible.field.widget.attrs['onchange'] = 'preview()'
            visible.field.widget.attrs['hidden'] = 'True'


class UpdatePasswordForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Ancien mot de passe'}),
                               max_length=60, label='Ancien mot de passe')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('password', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if self.errors:
                if visible.errors:
                    visible.field.widget.attrs['class'] = 'form-control is-invalid'
                else:
                    visible.field.widget.attrs['class'] = 'form-control is-valid'

            visible.field.widget.attrs['id'] = 'floatingInput'

    def clean(self):
        super(UpdatePasswordForm, self).clean()
        # Recuperation des champs du formulaire
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1:
            if not any(character.isdigit() for character in password1):
                self.add_error('password1', 'Le mot de passe doit contenir au moins un chiffre')

            if len(password1) < 6:
                self.add_error('password1', 'Le mot de passe doit avoir au moins 6 caracteres')

        return self.cleaned_data
