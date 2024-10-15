from django.shortcuts import render

# Create your views here
from rest_framework import generics
from .models import Book, UserProfile, Transaction
from .serializers import BookSerializer, UserProfileSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'isbn']
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'published_date']


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class CheckOutBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.number_of_copies > 0:
                transaction = Transaction.objects.create(
                        user=request.user,
                        book=book,
                        checkout_date=timezone.now()
                )
                book.number_of_copies -= 1
                book.save()
                return Response({'message': 'Book checked out successfully!'], status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Book checked out successfully!'}, status=status.HTTP_400_BAD_REQUEST)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user, return_date__isnull=True)
            transaction.return_date = timezone.now()
            transaction.save()

            book = transaction.book
            book.number_of_copies += 1
            book.save()

            return Response({'message': 'Book returned successfuly!'}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({'error': 'No active transaction found for this book.'}, status=status.HTTP_400_BAD_REQUEST)

