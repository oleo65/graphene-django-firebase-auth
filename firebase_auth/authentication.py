from django.contrib.auth import get_user_model
from firebase_admin import auth

from firebase_auth.apps import firebase_app


User = get_user_model()


class FirebaseAuthentication:

    def _get_auth_token(self, request):
        encoded_token = request.META.get('HTTP_AUTHORIZATION')
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(encoded_token, firebase_app)
        except ValueError:
            pass
        except auth.AuthError:
            pass
        return decoded_token

    def _get_user_from_firebase_user(self, firebase_user):
        firebase_uid = firebase_user.get('uid')
        user = None

        try:
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            user = self._register_unregistered_user(firebase_user)
        return user

    def _register_unregistered_user(self, firebase_user):
        user = None

        user = self._match_user_by_email(firebase_user)

        if user is None:
            user = User.objects.create_user(
                username=firebase_user['uid'], 
                email=firebase_user['email'], 
                )

        return user

    def _match_user_by_email(self, firebase_user):
        user = None

        try:
            user = User.objects.get(email=firebase_user['email'])
            user.firebase_uid = firebase_user['uid']
            user.save()
        except User.DoesNotExist:
            pass

        return user

    def authenticate(self, request):
        user = None
        firebase_user = self._get_auth_token(request)

        if firebase_user:
            user = self._get_user_from_firebase_user(firebase_user)
        return user

    def get_user(self, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user = None
        return user
