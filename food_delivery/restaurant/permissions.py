# restaurant/permissions.py
from rest_framework.permissions import BasePermission

class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow only the owner of the restaurant to access it
        restaurant_id = view.kwargs.get('restaurant_id')  # or use a different method to get the restaurant ID
        restaurant = restaurant.objects.filter(id=restaurant_id).first()

        if restaurant and restaurant.owner == request.user:
            return True
        
        return False