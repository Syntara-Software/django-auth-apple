=====
Django Auth Apple
=====

Auth Apple is a Django app to Sign up / Log in using Apple SignIn

Quick start
-----------

1. Add "google_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'apple_auth.apps.AppleAuthConfig',
    ]

2. Set the Apple variables::

    APPLE = {
        'KEY_ID': 'ID',
        'TEAM_ID': 'ID_TEAM',
        'CLIENT_ID': 'com.example.app',
        'RECEIPT_URL': 'https://sandbox.itunes.apple.com/verifyReceipt',
        'APP_SECRET': 'secret',
        'PRIVATE_KEY': """-----BEGIN PRIVATE KEY-----
    key
    -----END PRIVATE KEY-----"""
    }

3. Create a subclass of ``AppleAuth`` overriding the method ``get_user``::

    from apple_auth.models import NameComponents

    class ProjectAppleAuth(AppleAuth):

        def get_user(self, name: NameComponents, email):
            return User.objects.create_user(name.nickname, email, first_name=name.givenName,
                                            last_name=name.familyName)

In this method you get or create an instance of ``django.contrib.auth.models.User`` and make any additional configuration
needed by your project.

4. Run ``python manage.py migrate`` to create the apple-auth models.
