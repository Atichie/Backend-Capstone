from django.contrib import admin

# Register your models here.
from .models import UserProfile, Book, Transaction

admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(Transaction)
