from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    """Custom token based authorization.

    This class provide support to authorize requests using
    tokens inside querystring or headers of request.

    Note: The querystring has priority over header argument.

    See: https://github.com/tomchristie/django-rest-framework/
         blob/master/rest_framework/authentication.py#L143
    """

    def authenticate(self, request):
        token = request.GET.get('token')
        if token:
            return self.authenticate_credentials(key=token)
        else:
            return super(CustomTokenAuthentication, self).authenticate(request)
