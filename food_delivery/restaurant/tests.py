# restaurant/tests.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Restaurant, MenuItem, Order

class RestaurantAPITests(TestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.login(username='testuser', password='password')
        
        # Create a restaurant
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', owner=self.user)
        self.menu_item = MenuItem.objects.create(name='Pizza', price=10, restaurant=self.restaurant)

    def test_create_restaurant(self):
        """Test creating a restaurant via the API"""
        url = '/api/restaurant/restaurants/'
        data = {'name': 'New Restaurant', 'owner': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_menu_item(self):
        """Test creating a menu item for a restaurant"""
        url = '/api/restaurant/menu-items/'
        data = {'name': 'Burger', 'price': 5, 'restaurant': self.restaurant.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order(self):
        """Test creating an order for a restaurant"""
        url = '/api/restaurant/orders/'
        data = {'menu_item': self.menu_item.id, 'status': 'accepted'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order_status(self):
        """Test updating order status"""
        url = '/api/restaurant/orders/{}/update_status/'.format(self.menu_item.id)
        data = {'status': 'preparing'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'preparing')

    def test_register_user(self):
        """Test user registration"""
        url = '/api/restaurant/register/'
        data = {
            'username': 'newuser',
            'password': 'password123',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """Test user login"""
        url = '/api/restaurant/login/'
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
