from django import forms
from Store.models import *
from multiupload.fields import MultiImageField


class ajout_produitFrom(forms.ModelForm):
    class Meta:
        model = Produits
        exclude = ['author', 'date_created', 'starred', 'word_count', 'prix_promo', 'promotion_prod', 'vendu']
        widgets = {
            'details_prod': forms.Textarea(attrs={'placeholder': 'details du produit', 'rows': '5', }, ),
        }

    def __init__(self, *args, **kwargs):
        super(ajout_produitFrom, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if self.errors:
                if visible.errors:
                    visible.field.widget.attrs['class'] = 'form-control is-invalid'
                else:
                    visible.field.widget.attrs['class'] = 'form-control is-valid'

            visible.field.widget.attrs['id'] = 'floatingInput'

    def clean(self):
        super(ajout_produitFrom, self).clean()
        # Recuperation des champs du formulaire
        designation = self.cleaned_data.get('designation')
        categorie = self.cleaned_data.get('categorie_prod')
        etat = self.cleaned_data.get('etat_prod')
        details = self.cleaned_data.get('details_prod')
        ville = self.cleaned_data.get('ville_prod')
        prix = self.cleaned_data.get('prix_prod')
        promotion = self.cleaned_data.get('promotion_prod')
        # Gestion des erreurs

        if designation:
            if len(designation) < 3:
                self.add_error('designation', 'Designation du produit trop court (doit etre au moins 3 caracteres)')

        if prix:
            if prix < 500:
                self.add_error('prix_prod', 'Désolé, les produits doivent etre au moins a 500XAF')


class photo_produitsForm(forms.ModelForm):
    photo = MultiImageField(min_num=1, max_num=8)
    class Meta:
        model = Photo
        fields = ['photo', ]

    def __init__(self, *args, **kwargs):
        super(photo_produitsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['data-max_length'] = '7'
            visible.field.widget.attrs['multiple'] = 'True'

    def clean(self):
        super(photo_produitsForm, self).clean()
        # Recuperation des champs du formulaire
        photo = self.cleaned_data.get('photo')

        if photo:
            if len(photo) > 7:
                self.add_error('photo', 'Impossible de charger plus de 7 photos')


class delete_image(forms.Form):
    delete_image = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class vendu_produit(forms.ModelForm):
    class Meta:
        model = Produits
        fields = ['vendu', ]

    widgets = {
        'vendu': forms.BooleanField()
    }


class ajout_panierForm(forms.ModelForm):
    class Meta:
        model = Panier
        fields = ['Acheteur', 'Vendeur', 'produit']

