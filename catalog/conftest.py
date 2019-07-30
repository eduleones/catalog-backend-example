import pytest

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = User(
        username='test',
        email='test@test.com'
    )
    user.set_password('1qw23er4')
    user.save()
    return user


@pytest.fixture
def user_staff():
    user = User(
        username='test_admin',
        email='test_admin@test.com',
        is_staff=True
    )
    user.set_password('1qw23er4')
    user.save()
    return user


@pytest.fixture
def token(user):
    token = Token.objects.create(user=user)
    return token


@pytest.fixture
def token_staff(user_staff):
    token = Token.objects.create(user=user_staff)
    return token


@pytest.fixture
def authorized_client(api_client, token):
    token_header = 'Token {}'.format(token.key)
    api_client.credentials(HTTP_AUTHORIZATION=token_header)
    return api_client


@pytest.fixture
def authorized_staff_client(api_client, token_staff):
    token_header = 'Token {}'.format(token_staff.key)
    api_client.credentials(HTTP_AUTHORIZATION=token_header)
    return api_client
