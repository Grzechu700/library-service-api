from rest_framework import serializers
from .models import Borrowing
from books.serializers import BookSerializer


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowing
        fields = ["id", "borrow_date", "expected_return_date",
                  "actual_return_date", "book", "user"]
        read_only_fields = ["id", "borrow_date", "user"]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating borrowings"""

    class Meta:
        model = Borrowing
        fields = ("id", "expected_return_date", "book")
        read_only_fields = ("id",)

    def validate_book(self, value):
        """Check if book has available inventory"""
        if value.inventory <= 0:
            raise serializers.ValidationError(
                "This book is currently unavailable (no copies in inventory)."
            )
        return value

    def create(self, validated_data):
        """Create borrowing and decrease book inventory"""
        book = validated_data["book"]

        # Decrease inventory
        book.inventory -= 1
        book.save()

        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("Authentication required")
        validated_data["user"] = request.user

        return super().create(validated_data)
