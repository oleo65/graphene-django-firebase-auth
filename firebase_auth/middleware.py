from django.contrib.auth import authenticate
from .decorators import one_time_middleware
from .settings import firebase_auth_settings

class FirebaseAuthGrapheneMiddleware():
    """Middleware to be used with graphene to authenticate the firebase user via token."""

    @one_time_middleware
    def resolve(self, next_chain, root, info, **kwargs):
        context = info.context
        token = self._get_token(context)

        if token is not None:
            user = authenticate(request=context)

            if user is not None:
                context.user = user

        return next_chain(root, info, **kwargs)

    def _get_token(self, context):
        auth_data = context.META.get(firebase_auth_settings.AUTH_HEADER_NAME, '').split()

        if len(auth_data) == 1 and auth_data[0] != '':
            return auth_data[0]
        elif len(auth_data) == 2:
            return auth_data[1]

        return None
