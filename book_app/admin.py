from django.contrib import admin
from .models import LibraryUser, Author, Publisher, Book

admin.site.register(LibraryUser)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
