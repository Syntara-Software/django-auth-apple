=====
Django Auth Apple
=====

Auth Apple is a Django app to Sign up / Log in using Apple SignIn

Quick start
-----------

1. Install::

    pip install git+https://JuanJoseArreola@bitbucket.org/osyres/django-auth-apple.git@0.7.0

or add it to your requirements.txt::

    git+https://JuanJoseArreola@bitbucket.org/osyres/django-auth-apple.git@0.7.0


2. Add "google_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'apple_auth.apps.AppleAuthConfig',
    ]

3. Set the Apple variables::

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

4. Create a subclass of ``AppleAuth`` overriding the method ``get_user``::

    from apple_auth.models import NameComponents

    class CustomAppleAuth(AppleAuth):

        def get_user(self, components: NameComponents, email):
            try:
                return Customer.objects.get(user__email=email).user
            except Customer.DoesNotExist:
                user = User.objects.create_user(components.nickname, email, first_name=components.givenName,
                                                last_name=components.familyName)
                Customer.objects.create(user=user)
                return user

In this method you get or create an instance of ``django.contrib.auth.models.User`` and make any additional configuration
needed by your project.

5. Run ``python manage.py migrate`` to create the apple-auth models.

6. Use it to authenticate the users::

    def post(self, request):
        serializer = AppleSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credentials = serializer.save()

        social_user, created = self.social_manager.login_or_signup(credentials)

        # response
