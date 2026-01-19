import pytest
from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from borrowings.models import Borrowing

User = get_user_model()


@pytest.mark.django_db
class TestBorrowings:

    def test_create_borrowing_success(self, auth_client, book):
        """Test creating borrowing - happy path"""
        url = reverse('borrowing-list')
        data = {
            'book': book.id,
            'expected_return_date': (date.today() + timedelta(days=7)).isoformat()
        }
        response = auth_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        book.refresh_from_db()
        assert book.inventory == 4

    def test_create_borrowing_no_inventory(self, auth_client, book):
        """Test creating borrowing when no inventory"""
        book.inventory = 0
        book.save()

        url = reverse('borrowing-list')
        data = {
            'book': book.id,
            'expected_return_date': (date.today() + timedelta(days=7)).isoformat()
        }
        response = auth_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_borrowing_success(self, auth_client, user, book):
        """Test returning borrowing - happy path"""
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return_date=date.today() + timedelta(days=7)
        )

        url = reverse('borrowing-return-borrowing', kwargs={'pk': borrowing.id})
        response = auth_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        borrowing.refresh_from_db()
        assert borrowing.actual_return_date is not None
        book.refresh_from_db()
        assert book.inventory == 6

    def test_return_already_returned(self, auth_client, user, book):
        """Test returning already returned borrowing"""
        borrowing = Borrowing.objects.create(
            user=user,
            book=book,
            expected_return_date=date.today() + timedelta(days=1),
            actual_return_date=date.today() + timedelta(days=1)
        )

        url = reverse('borrowing-return-borrowing', kwargs={'pk': borrowing.id})
        response = auth_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_sees_own_borrowings(self, auth_client, user, book):
        """Test user sees only own borrowings"""
        Borrowing.objects.create(
            user=user,
            book=book,
            expected_return_date=date.today() + timedelta(days=1)
        )

        other_user = User.objects.create_user(email="other@test.com", password="pass")
        Borrowing.objects.create(
            user=other_user,
            book=book,
            expected_return_date=date.today() + timedelta(days=1)
        )

        url = reverse('borrowing-list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_admin_sees_all_borrowings(self, admin_client, user, book):
        """Test admin sees all borrowings"""
        Borrowing.objects.create(
            user=user,
            book=book,
            expected_return_date=date.today() + timedelta(days=1)
        )

        other_user = User.objects.create_user(email="other@test.com", password="pass")
        Borrowing.objects.create(
            user=other_user,
            book=book,
            expected_return_date=date.today() + timedelta(days=1)
        )

        url = reverse('borrowing-list')
        response = admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
