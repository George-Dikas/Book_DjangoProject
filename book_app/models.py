from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class LibraryUser(models.Model): 
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ["user__last_name"]
                      
    def __str__(self):
        return (self.user.last_name + ' ' + self.user.first_name)

class Author(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18')
        ]

        ordering = ["user__last_name"]

    def __str__(self):
        return (self.user.last_name + ' ' + self.user.first_name)

class Publisher(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=30)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pub_date = models.DateField()
    num_stars = models.DecimalField(default=0, max_digits=3, decimal_places=2, 
                                    validators=[MinValueValidator(0), MaxValueValidator(5)])
    num_rates = models.IntegerField(default=0)
    book = models.FileField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Favourite(models.Model):
    lib_user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title
        