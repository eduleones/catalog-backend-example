import pytest

from django.test import RequestFactory

from rest_framework.exceptions import AuthenticationFailed

from drf.authentication import CustomTokenAuthentication


@pytest.mark.django_db
class TestCustomTokenAuthentication:

    def setup(self):
        self.factory = RequestFactory()
        self.authentication = CustomTokenAuthentication()

    def test_auth_by_querystring(self, token):
        url = '/test?token={}'.format(token.key)
        request = self.factory.get(url)
        result = self.authentication.authenticate(request=request)
        assert result[0]  # user authenticated

    def test_auth_by_querystring_invalid_token(self):
        url = '/test?token=batatinha'
        request = self.factory.get(url)
        with pytest.raises(AuthenticationFailed):
            self.authentication.authenticate(request=request)

    def test_auth_by_header(self, token):
        url = '/test'
        authorization = 'Token {}'.format(token.key)
        request = self.factory.get(url, HTTP_AUTHORIZATION=authorization)
        result = self.authentication.authenticate(request=request)
        assert result[0]  # user authenticated

    def test_auth_by_header_invalid_token(self):
        url = '/test'
        authorization = 'Token batatinha'
        request = self.factory.get(url, HTTP_AUTHORIZATION=authorization)
        with pytest.raises(AuthenticationFailed):
            self.authentication.authenticate(request=request)
