from dataclasses import dataclass

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppleUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    subject = models.CharField(_('Subject'), max_length=64)
    token = models.TextField(_('Token'))
    accessToken = models.TextField(_('Access token'))
    refreshToken = models.TextField(_('Refresh token'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} [{self.subject}]'

    class Meta:
        ordering = ['-created']


@dataclass
class NameComponents:
    namePrefix: str = None
    givenName: str = None
    middleName: str = None
    familyName: str = None
    nameSuffix: str = None
    nickname: str = None

    def get_full_name(self):
        return f'{self.givenName or ""} {self.familyName or ""}'.strip()


@dataclass
class AppleCredentials:
    token: str
    name: NameComponents = None
