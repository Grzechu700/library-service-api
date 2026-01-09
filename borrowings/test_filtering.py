import pytest
from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from borrowings.models import Borrowing

User = get_user_model()


@pytest.mark.django_db
class TestFiltering:

    def test_filter_by_is_active(self, auth_client, user, book):
        """Test filtering by active status"""
        active = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return_date=date.today() + timedelta(days=7)
        )

        returned = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return_date=date.today() + timedelta(days=1),
            actual_return_date=date.today() + timedelta(days=1)
        )

        url = reverse('borrowing-list')

        # Test active filter
        response = auth_client.get(url, {'is_active': 'true'})
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == active.id

        # Test returned filter
        response = auth_client.get(url, {'is_active': 'false'})
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == returned.id

    def test_admin_filter_by_user_id(self, admin_client, book):
        """Test admin can filter by user_id"""
        user1 = User.objects.create_user(email="user1@test.com", password="pass")
        user2 = User.objects.create_user(email="user2@test.com", password="pass")

        Borrowing.objects.create(
            user=user1,
            book=book,
            expected_return_date=date.today() + timedelta(days=1)
        )
        Borrowing.objects.create(
            user=user2,
            book=book,
            expected_return_date=date.today() + timedelta(days=1)
        )

        url = reverse('borrowing-list')
        response = admin_client.get(url, {'user_id': user1.id})

        assert response.data['count'] == 1
