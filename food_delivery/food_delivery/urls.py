"""
URL configuration for food_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import get_resolver


def home(request):
    return HttpResponse("Welcome to the Food Delivery API")

def list_urls(request):
    resolver = get_resolver()
    url_patterns = []
    for pattern in resolver.reverse_dict.keys():
        if isinstance(pattern, str):  # Filter for valid URL patterns
            url_patterns.append(pattern)
    return JsonResponse({'urls': url_patterns})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/restaurant/', include('restaurant.urls')), 
    path('api/customer/', include('customer.urls')),
    path('api/admin/customer/', include('customer.urls')),
    path('', home),
   
    
]

urlpatterns += [
    path('debug/urls/', list_urls),  # Temporary endpoint
]
