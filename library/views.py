from django.shortcuts import render

# Create your views here
from rest_framework import generics
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Book, UserProfile, Transaction
from .serializers import BookSerializer, UserProfileSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from .serializers import SignInSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.http import JsonResponse

class SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request, user)
                return Response({'success': 'Logged in successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
           
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Logged in successfully!'})
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=400)


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
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

            if book.number_of_copies <= 0:
                return Response({'error':' No copies available for checkout.'}, status=status.HTTP_400_BAD_REQUEST)

                transaction = Transaction.objects.create(
                        user=request.user,
                        book=book,
                        checkout_date=timezone.now()
                )

                book.number_of_copies -= 1
                book.save()

                return Response({'success': 'Book checked out successfully!', 'transaction_id': transaction.id}, status=status.HTTP_201_CREATED)
    

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

class UserProfileRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]



