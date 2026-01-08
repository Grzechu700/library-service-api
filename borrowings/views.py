from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Borrowing
from .serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """List, Detail and Create borrowings"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")

        user_id = self.request.query_params.get("user_id")
        if user_id is not None and self.request.user.is_staff:
            queryset = queryset.filter(user_id=user_id)
        elif not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def get_serializer_class(self):
        """Use different serializers for read and write operations"""
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active borrowings (not returned yet). Example: ?is_active=true",
                required=False,
            ),
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                description="Filter by user ID (admin only). Example: ?user_id=3",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """List borrowings with optional filters"""
        return super().list(request, *args, **kwargs)
