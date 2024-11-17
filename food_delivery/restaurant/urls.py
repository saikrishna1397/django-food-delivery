# restaurant/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuItemViewSet, OrderViewSet,RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),  # Registration
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Login (Token Generation)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token Refresh
    path('api/', include(router.urls))
    
]





