from django.contrib import admin
from clients.models import Client
from clients.models import SocialNetwork

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
#la renombramos porque ya tengo mi propio UserAdmin y este el de arriba es de django

class ClientAdmin(admin.ModelAdmin):
    exclude = ('user',)

class ClientInLine(admin.StackedInline):
    model = Client
    can_delete = False

class SocialInLine(admin.StackedInline):
    model = SocialNetwork
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [ClientInLine, SocialInLine]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
