# restaurant/models.py
from django.contrib.auth.models import User
from django.db import models

class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurants")
    name = models.CharField(max_length=255)
    address = models.TextField()
    hours_of_operation = models.CharField(max_length=255)
    delivery_zones = models.TextField()  # List of delivery zones
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=50, choices=[('accepted', 'Accepted'), ('preparing', 'Preparing'), ('ready', 'Ready for delivery')])
    # other fields like customer, items, total price, etc.
