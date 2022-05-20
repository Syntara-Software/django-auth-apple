from django.contrib import admin
from django.contrib.admin import register

from apple_auth.models import AppleUser


@register(AppleUser)
class AppleUserAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'created']
