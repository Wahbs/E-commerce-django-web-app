from multiupload.fields import MultiImageField

from Discussion.models import chatMessages
from django import forms


class EnvoieMessage_Form(forms.ModelForm):
    class Meta:
        model = chatMessages
        fields = ['message', ]


class EnvoieFichier_form(forms.ModelForm):
    photo = MultiImageField(min_num=1, max_num=8)

    class Meta:
        model = chatMessages
        fields = ['photo', ]

    def __init__(self, *args, **kwargs):
        super(EnvoieFichier_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['data-max_length'] = '7'
            visible.field.widget.attrs['multiple'] = 'True'
            visible.field.widget.attrs['hidden'] = 'True'