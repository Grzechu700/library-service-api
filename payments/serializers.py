from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing_id = serializers.IntegerField(source="borrowing.id", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "status_display",
            "type",
            "type_display",
            "borrowing",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PaymentListSerializer(serializers.ModelSerializer):
    borrowing_id = serializers.IntegerField(source="borrowing.id", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing_id",
            "money_to_pay",
            "created_at"
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        ]

    def validate_money_to_pay(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
