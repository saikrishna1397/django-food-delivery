# restaurant/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Restaurant, MenuItem, Order
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer,RegisterSerializer
from .permissions import IsRestaurantOwner
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User





class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        return self.queryset.filter(restaurant__owner=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        return self.queryset.filter(restaurant__owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get("status")
        if status not in ['accepted', 'preparing', 'ready']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status
        order.save()
        return Response(OrderSerializer(order).data)





class RegisterView(APIView):
    def post(self, request):
        # Assuming RegisterSerializer handles user creation correctly
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save user and generate tokens
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            # Return the response with user data and JWT tokens
            return Response({
                "user": serializer.data,  # Include user data
                "refresh": str(refresh),  # Refresh token
                "access": str(refresh.access_token)  # Access token
            }, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
