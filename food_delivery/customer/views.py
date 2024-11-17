import requests
from rest_framework import status, views, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from rest_framework import status
from customer.models import  CustomerProfile, Order, OrderItem
from customer.serializers import InternalOrderSerializer
from .serializers import (
     CustomerProfileSerializer,
    CustomerOrderSerializer,RegisterSerializer,OrderSerializer,CustomerSerializer
)
from restaurant.models import Restaurant, MenuItem
from restaurant.serializers import RestaurantSerializer, MenuItemSerializer
from .permissions import IsAdminUser
from django.contrib.auth.models import User

class CustomerRegisterView(views.APIView):
    permission_classes = []
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return CustomerProfile.objects.get(user=self.request.user)

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuViewSet(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(restaurant_id=restaurant_id)

class SearchMenuItems(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return MenuItem.objects.filter(name__icontains=query)

class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class TrackOrderView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Order.objects.get(id=self.kwargs['order_id'], customer=self.request.user)

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
class CustomerOrderView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomerOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            orderId = serializer.validated_data['orderId']
            foodItems = serializer.validated_data['foodItems']
            totalAmount = serializer.validated_data['totalAmount']
            customerName = serializer.validated_data['customerName']
            deliveryAddress = serializer.validated_data['deliveryAddress']
            paymentMethod = serializer.validated_data['paymentMethod']

            # Prepare payload for the downstream API
            downstream_payload = {
                "orderId": orderId,
                "foodItems": foodItems,
                "totalAmount": totalAmount,
                "customerName": customerName,
                "deliveryAddress": deliveryAddress,
                "paymentMethod": paymentMethod,
            }
            headers = {"Authorization": f"Bearer {request.auth}"}

            # Replace with the actual downstream API URL
            downstream_url = "http://example.com/external-api/orders/"
            try:
                response = requests.post(downstream_url, json=downstream_payload, headers=headers)
                if response.status_code == 200:
                    return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": response.json()}, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return Response({"error": "Failed to place order.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class CustomerListView(generics.ListAPIView):
    """
    API to list all customers (admin only).
    """
    queryset = User.objects.filter(is_staff=False, is_active=True)  # Exclude admin and inactive users
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CustomerEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    API to view, update, or soft-delete a specific customer (admin only).
    """
    queryset = User.objects.filter(is_staff=False, is_active=True)  # Exclude admin and inactive users
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.is_active = False  
        customer.save()
        return Response({"message": "Customer deactivated successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class PlaceOrderView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InternalOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Build the payload for the external API
            payload = serializer.validated_data
            restaurant_id = self.request.query_params.get("restaurantId")

            if not restaurant_id:
                return Response(
                    {"error": "Restaurant ID is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            external_api_url = f"http://ec2-13-201-97-212.ap-south-1.compute.amazonaws.com:8080/add/orders?restaurantId={restaurant_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer your_auth_token_here"
            }

            # Send POST request to the external API
            try:
                response = requests.post(
                    external_api_url, json=payload, headers=headers
                )
                return Response(response.json(), status=response.status_code)
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": "Failed to connect to the external API", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
