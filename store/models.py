from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    SIZES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    CATEGORIES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('accessories', 'Accessories'),
    ]
    STATUS = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('in_cart', 'In Cart'),
    ]

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="imgs/", blank=False, null=False)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    size = models.CharField(max_length=10, choices=SIZES)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='available')

    def __str__(self):
        return self.name
    
class Store(models.Model):
    name = models.CharField(max_length=50)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name
 
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Cart for {self.user}"

class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Order {self.id} for {self.user}"