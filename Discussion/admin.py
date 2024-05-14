from django.contrib import admin
from Discussion.models import chatMessages

# Register your models here.


class MsgAdmin(admin.ModelAdmin):
    list_display = ('message', 'produit')


admin.site.register(chatMessages, MsgAdmin)