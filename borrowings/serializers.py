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
        if value.inventory == 0:
            raise serializers.ValidationError(
                "This book is currently unavailable (inventory is 0)."
            )
        return value

    def create(self, validated_data):
        """Create borrowing and decrease book inventory"""
        book = validated_data["book"]

        # Decrease inventory
        book.inventory -= 1
        book.save()

        # Attach current user (from context)
        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)
