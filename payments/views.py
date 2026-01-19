from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentCreateSerializer
)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments.

    Provides CRUD operations and custom actions for payment management.
    Non-staff users can only see their own payments.
    """
    queryset = Payment.objects.select_related("borrowing", "borrowing__user", "borrowing__book")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "list":
            return PaymentListSerializer
        elif self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_queryset(self):
        """
        Filter queryset based on user permissions and query parameters.

        Filters:
        - status: Filter by payment status (PENDING/PAID)
        - type: Filter by payment type (PAYMENT/FINE)
        """
        queryset = Payment.objects.select_related(
            "borrowing",
            "borrowing__user",
            "borrowing__book"
        )

        # Non-staff users can only see their own payments
        if not self.request.user.is_staff:
            queryset = queryset.filter(borrowing__user=self.request.user)

        # Apply optional filters
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)

        type_param = self.request.query_params.get("type")
        if type_param:
            queryset = queryset.filter(type=type_param)

        return queryset

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        """
        Mark a payment as paid.

        Returns error if payment is already paid.
        """
        payment = self.get_object()

        if payment.status == Payment.Status.PAID:
            return Response(
                {"detail": "Payment is already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = Payment.Status.PAID
        payment.save()

        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my_payments(self, request):
        """Get all payments for the authenticated user."""
        payments = Payment.objects.select_related(
            "borrowing",
            "borrowing__user",
            "borrowing__book"
        ).filter(borrowing__user=request.user)

        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        """Get all pending payments visible to the current user."""
        queryset = self.get_queryset().filter(status=Payment.Status.PENDING)
        serializer = PaymentListSerializer(queryset, many=True)
        return Response(serializer.data)
