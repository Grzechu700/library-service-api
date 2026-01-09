import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPermissions:

    def test_admin_can_create_books(self, admin_client):
        """Test admin can create books"""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'Author',
            'cover': 'SOFT',
            'inventory': 10,
            'daily_fee': 2.00
        }
        response = admin_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_user_cannot_create_books(self, auth_client):
        """Test regular user cannot create books"""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'Author',
            'cover': 'SOFT',
            'inventory': 10,
            'daily_fee': 2.00
        }
        response = auth_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthorized_cannot_access_borrowings(self, api_client):
        """Test unauthorized cannot access borrowings"""
        url = reverse('borrowing-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthorized_cannot_create_borrowings(self, api_client):
        """Test unauthorized user cannot create borrowings"""
        url = reverse('borrowing-list')
        data = {
            'book': 1,
            'expected_return_date': '2026-01-20'
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
