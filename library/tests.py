from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Book
from rest_framework import status
from rest_framework.test import APIClient


class BookTests(APITestCase):
    def setup(self):
        self.book = Book.objects.create(
                title="1984",
                author="George Orwell",
                isbn="9780451524935",
                published_date="1949-06-08",
                number_of_copies=10
       )

    def test_list_books(self):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "1984")

    def test_create_book(self):
        data = {
                "title": "Brave New World",
                "author": "Aldous Huxley",
                "isbn": "9780060850524",
                "published_date": "1932-08-01",
                "number_of_copies": 8
        }
    def test_get_books(self):
        self.response = self.client.post(reverse('book-list'), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

