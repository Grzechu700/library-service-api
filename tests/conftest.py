import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from books.models import Book
from borrowings.models import Borrowing

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@test.com",
        password="testpass123"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@test.com",
        password="adminpass123"
    )


@pytest.fixture
def auth_client(api_client, user):
    # Test fixture - token generated dynamically, not a hardcoded secret
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    # Test fixture - token generated dynamically, not a hardcoded secret
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZE=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def book(db):
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover="HARD",
        inventory=5,
        daily_fee=1.50
    )
