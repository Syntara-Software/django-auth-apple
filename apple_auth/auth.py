from abc import ABC, abstractmethod
from datetime import timedelta

import jwt
import requests
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apple_auth.models import AppleUser, AppleCredentials, NameComponents
from core.exceptions import UserInputError


class AppleAuth(ABC):

    def __init__(self, client_id=settings.APPLE['CLIENT_ID']):
        self.client_id = client_id

    def login_or_signup(self, credentials: AppleCredentials):
        response, info = self.validate_access_token(credentials.token)
        try:
            apple_user = AppleUser.objects.get(subject=info['sub'])
            return self._update_token(credentials, response, apple_user), False
        except AppleUser.DoesNotExist:
            return self.signup(info, response, credentials), True

    def _update_token(self, credentials: AppleCredentials, response, apple_user):
        apple_user.token = credentials.token
        apple_user.accessToken = response.get('access_token')
        apple_user.refreshToken = response.get('refresh_token')
        apple_user.save()
        return apple_user

    def signup(self, info, response, credentials: AppleCredentials):
        user = self.get_user(credentials.name, info['email'])
        return AppleUser.objects.create(user=user, subject=info['sub'],
                                        token=credentials.token,
                                        accessToken=response.get('access_token'),
                                        refreshToken=response.get('refresh_token'))

    @abstractmethod
    def get_user(self, components: NameComponents, email):
        pass

    def validate_access_token(self, token):
        response = self.authenticate_token(token)
        if not (info := self.get_user_info(response)):
            raise UserInputError(_("It wasn't possible to get the account details"),
                                 'apple.invalid_id_token')
        if info['aud'] != self.client_id:
            raise UserInputError(_("It wasn't possible to validate the account"),
                                 'apple.invalid_client')
        return response, info

    def authenticate_token(self, token):
        url = 'https://appleid.apple.com/auth/token'
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': self.client_id,
            'client_secret': self.get_client_secret(),
            'code': token,
            'grant_type': 'authorization_code',
        }
        response = requests.post(url, data, headers=headers)
        response.raise_for_status()

        return response.json()

    def validate_refresh_token(self, token):
        url = 'https://appleid.apple.com/auth/token'
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': self.client_id,
            'client_secret': self.get_client_secret(),
            'grant_type': 'authorization_code',
            'refresh_token': token,
        }
        response = requests.post(url, data, headers=headers)
        response.raise_for_status()

        return response.json()

    def get_client_secret(self):
        headers = {
            'kid': settings.APPLE['KEY_ID']
        }
        payload = {
            'iss': settings.APPLE['TEAM_ID'],
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': self.client_id,
        }
        return jwt.encode(payload, settings.APPLE['PRIVATE_KEY'], algorithm='ES256',
                          headers=headers)

    def get_user_info(self, json_response):
        if id_token := json_response.get('id_token', None):
            return jwt.decode(id_token, '', algorithms=['ES256'], verify=False)
