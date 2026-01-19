from django.db import models
from decimal import Decimal


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.PAYMENT
    )
    borrowing = models.ForeignKey(
        "borrowings.Borrowing",
        on_delete=models.CASCADE,
        related_name="payments"
    )
    session_url = models.URLField(
        max_length=500,
        help_text="URL to Stripe payment session"
    )
    session_id = models.CharField(
        max_length=255,
        help_text="Stripe payment session ID"
    )
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount in USD"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.id} - {self.type} - ${self.money_to_pay}"
