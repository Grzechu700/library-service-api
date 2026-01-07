from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Borrowing
from .serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """List, Detail and Create borrowings"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user).select_related("book", "user")

    def get_serializer_class(self):
        """Use different serializers for read and write operations"""
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer
