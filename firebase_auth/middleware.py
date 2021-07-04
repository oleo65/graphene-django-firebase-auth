from django.contrib.auth import authenticate

AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"


class FirebaseAuthGrapheneMiddleware():
    """Middleware to be used with graphene to authenticate the firebase user via token."""

    def resolve(self, next_chain, root, info, **kwargs):
        context = info.context
        token = self.get_token(context)

        if token is not None:
            user = authenticate(request=context)

            if user is not None:
                context.user = user

        return next_chain(root, info, **kwargs)

    def get_token(self, context):
        auth_data = context.META.get(AUTH_HEADER_NAME, '').split()

        if len(auth_data) == 1 and auth_data[0] != '':
            return auth_data[0]
        elif len(auth_data) == 2:
            return auth_data[1]

        return None
