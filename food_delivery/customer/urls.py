from django.http import JsonResponse
from django.urls import get_resolver
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    PlaceOrderView, TrackOrderView,
    OrderHistoryView,CustomerOrderView,CustomerListView,CustomerEditView,
    CustomerRegisterView,CustomerProfileView,RestaurantViewSet,SearchMenuItems,MenuViewSet,PlaceOrderView
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')


urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('restaurants/<int:restaurant_id>/menu/', MenuViewSet.as_view(), name='restaurant-menu'),
    path('search/', SearchMenuItems.as_view(), name='search-menu'),
    path('order/', PlaceOrderView.as_view(), name='place-order'),
    path('order/<int:order_id>/track/', TrackOrderView.as_view(), name='track-order'),
    path('orders/', OrderHistoryView.as_view(), name='order-history'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customer-order/', CustomerOrderView.as_view(), name='customer-order'),
    path('api/admin/customers/', CustomerListView.as_view(), name='admin-customer-list'),
    path('api/admin/customers/<int:pk>/', CustomerEditView.as_view(), name='admin-customer-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/customer/order/', PlaceOrderView.as_view(), name='place-order-external-api'),
]+ router.urls

def list_urls(request):
    resolver = get_resolver()
    urls = list(resolver.reverse_dict.keys())
    return JsonResponse({'urls': urls})

urlpatterns += [
    path('debug/urls/', list_urls),  # Temporary endpoint
]
