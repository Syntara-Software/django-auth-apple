from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppleAuthConfig(AppConfig):
    name = 'apple_auth'

    verbose_name = _('Apple Auth')
