from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book

User = get_user_model()


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')

    class Meta:
        ordering = ['-borrow_date']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(expected_return_date__gt=models.F('borrow_date')),
                name='expected_return_after_borrow'
            ),
            models.CheckConstraint(
                condition=models.Q(actual_return_date__isnull=True) |
                      models.Q(actual_return_date__gte=models.F('borrow_date')),
                name='actual_return_after_borrow'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.book.title} ({self.borrow_date})"
