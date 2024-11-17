from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerProfile, Order, OrderItem
from restaurant.models import Restaurant, MenuItem

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        CustomerProfile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
        return user

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ('username','email','first_name','last_name')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menu_item', 'quantity')

class CustomerOrderSerializer(serializers.Serializer):
    orderId = serializers.CharField()
    restaurant = serializers.CharField()
    foodItems = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )
    totalAmount = serializers.FloatField()
    customerName = serializers.CharField()
    deliveryAddress = serializers.CharField()
    paymentMethod = serializers.CharField()

    def validate_restaurant(self, value):
        if not value:
            raise serializers.ValidationError("Restaurant ID is required.")
        return value 

    # This assumes that the customer is the authenticated user
    customer = serializers.PrimaryKeyRelatedField(queryset=CustomerProfile.objects.all(), default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        # Extract validated data
        restaurant = validated_data['restaurant']
        order_id = validated_data['orderId']
        food_items = validated_data['foodItems']
        total_amount = validated_data['totalAmount']
        customer_name = validated_data['customerName']
        delivery_address = validated_data['deliveryAddress']
        payment_method = validated_data['paymentMethod']
        customer = validated_data['customer']

        # Create the Order
        order = Order.objects.create(
            #restaurant=restaurant,
            order_id=order_id,
            total_amount=total_amount,
            customer_name=customer_name,
            delivery_address=delivery_address,
            payment_method=payment_method,
            #customer=customer
        )

        # Create the OrderItems
        for item in food_items:
            OrderItem.objects.create(
                order=order,
                food_id=item['foodId'],
                food_name=item['foodName'],
                quantity=item['quantity']
            )
        
        return order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['foodItems', 'totalAmount', 'customer', 'customerName', 'deliveryAddress', 'customerPhoneNo', 'paymentMethod']
        extra_kwargs = {
            'customer': {'required': False},  # Make this field optional
        }

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']


class InternalOrderSerializer(serializers.Serializer):
    foodItems = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )
    totalAmount = serializers.FloatField(required=True)
    customerId = serializers.CharField(required=True)
    customerName = serializers.CharField(required=True)
    deliveryAddress = serializers.CharField(required=True)
    customerPhoneNo = serializers.CharField(required=True)
    paymentMethod = serializers.CharField(required=True)

