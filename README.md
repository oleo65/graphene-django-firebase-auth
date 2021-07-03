# graphene-django-firebase-auth

Authentication provider for graphene-django and Firebase's Authentication service.

This code has been ported to Python 3.9 and extended to be used as a plug and play solution with graphene. It is still somewhat work in progress and contributions are welcome.

Partially inspired by
[django-firebase-auth](https://github.com/fcornelius/django-firebase-auth)
for Django REST framework.

This app is used with [Firebase Authentication](https://firebase.google.com/docs/auth/) on a client.

## Compatibility

This code has only been tested with Python `3.9.0` and Django `2.2.5`.

## Installing

1. Install the app:

```sh
pipenv install graphene-django-firebase-auth
```

2. Download the JSON file from your [Firebase console](https://console.firebase.google.com/) with your account's credentials.

3. Set `GOOGLE_APPLICATION_CREDENTIALS` in your project's settings to the path of the credentials file:

```python
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, 'path/to/google-service-account.json')
```

4. Add the authentication backend to `AUTHENTICATION_BACKENDS`:

```python
AUTHENTICATION_BACKENDS = ['firebase_auth.authentication.FirebaseAuthentication']
```

5. Add authentication middleware to `GRAPHENE`

```python
GRAPHENE = {
    'MIDDLEWARE': ['firebase_auth.middleware.FirebaseAuthGrapheneMiddleware',],
}
```

6. Add `firebase_auth` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
  '...',
  'firebase_auth',
]
```

7. Add `FirebaseAuthMixin` to your `AUTH_USER_MODEL`. You need to have a custom user model to make this work.:

```python
from django.contrib.auth.models import AbstractUser
from firebase_auth.models import FirebaseAuthMixin

class User(AbstractUser, FirebaseAuthMixin):
    pass
```

8. Build and run your DB migrations to add the changes:

```sh
./manage.py makemigrations
./manage.py migrate
```

## Using the package

Once installed, authentication will be managed using this package.

The `Firebase JWT Token` is extracted from the header and evaluated by the middleware. It is then send to the authorization backend(s) for validation and django user matching. If successful the `context.user` will be properly populated with the matched user and will be available for further processing.

You can access `info.context.user` to add authentication logic, such as
with the following:

```python
def resolve_users(self, info, **kwargs):
    success = False

    if info.context.user.is_authenticated:
        success = True
    return success
```

## Sending tokens from the client

Your client will need to send an additional HTTP header `Authorization: <Firebase Token>` on each request.

How you do this depends on your client and is outside the scope of this documentation.

## Developing

### Setting up your environment

1. Install the dependencies:

```sh
pipenv install -d
```

2. Download the JSON file from your [Firebase console](https://console.firebase.google.com/) with your account's credentials.

3. Create an `.env` file using `.env.example` as a template. Make sure
to specify the path to the file in the previous step.

4. Enter the virtual environment:

```sh
./manage.py shell
```

### Other commands

```sh
# Run the tests
./manage.py test
```

```sh
# Lint the code
./lint.sh
```
