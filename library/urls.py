from django.urls import path, include
from .views import SignInView
from .views import (
        BookListCreateView, BookRetrieveUpdateDestroyView,
        UserProfileListCreateView, UserProfileRetrieveUpdateDestroyView,
        CheckOutBookView, ReturnBookView
)

urlpatterns = [
        path('signin/', SignInView.as_view(), name='signin'),
        path('book/', BookListCreateView.as_view(), name='book-list'),
        path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
        path('users/', UserProfileListCreateView.as_view(), name='user-profile-list'),
        path('user-profile/<int:pk>/', UserProfileRetrieveUpdateDestroyView.as_view(), name='user-profile-detail'),
        path('books/<int:book_id>/checkout/', CheckOutBookView.as_view(), name='book-checkout'),
        path('transactions/<int:transaction_id>/return/', ReturnBookView.as_view(), name='book-return'),
]

