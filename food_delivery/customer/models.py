from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Restaurant, MenuItem

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #address = models.CharField(max_length=255,null=True, blank=True)
    first_name=models.CharField(max_length=255,null=True, blank=True)
    last_name=models.CharField(max_length=255,null=True, blank=True)
    username=models.CharField(max_length=255,null=True, blank=True)
    email=models.CharField(max_length=255,null=True, blank=True)
    
    

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.SET_NULL, null=True, blank=True)  # Make this optional
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

