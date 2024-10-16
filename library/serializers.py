from rest_framework import serializers
from .models import UserProfile, Book, Transaction
from rest_framework.views import APIView

class SignInSerializer(serializers.Serializer):
    def validate(self, attrs):
        """Check that the username and password are correct."""
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True, min_length=6)

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'date_of_membership', 'active_status']

    def validate_user(self,value):
        """Ensure the user is valid and active."""
        if not value.is_active:
            raise serializers.ValidationError("This user is not active.")
        return value

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'number_of_copies']

    def validate_isbn(self, value):
        """Check that the ISBN is unique."""
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("This ISBN is already in use.")
        return value
    
    def validate_number_of_copies(self, value):
        """Ensure that the number of copies is not negative."""
        if value < 0:
            raise serializers.ValidationError("Number of copies cannot be negative.")
        return attrs


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date']

    def validate(self,attrs):
        """Check that the book is available for checkout."""
        book = attrs.get('book')
        if book and book.number_of_copies <= 0:
            raise serializers.ValidationError("This book is not available for checkout.")
        return attrs
 
    def create(self, validated_data):
        """Override create method to handle book copy decrement,"""
        book = validated_data['book']
        if book.number_of_copies > 0:
            book.number_of_copies -= 1
            book.save()
        return super().create(validated_data)


    def update(self, instance, validated_data):
        """Override update method to handle return date."""
        if 'return_date' in validated_data:
            book = instance.book
            book.number_of_copies +=1
            book.save()
        return super().update(instance, validated_data)




