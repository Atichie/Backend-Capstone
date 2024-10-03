from rest_framework import serializers
from .models import UserProfile, Book, Transaction

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'date_of_membership', 'active_status']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'number_of_copies']

    def validate_isbn(self, value):
        """Check that the ISBN is unique."""
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("This ISBN is already in use.")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date']

