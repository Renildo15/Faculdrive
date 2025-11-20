import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(
            username=kwargs.get("username", "user"),
            email=kwargs.get("email", "user@email.com"),
            password=kwargs.get("password", "pass1234")
        )
    return make_user