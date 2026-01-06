from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Borrowing
from .serializers import BorrowingReadSerializer


class BorrowingViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """List and Detail only (no create/update/delete yet)"""
    serializer_class = BorrowingReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)
