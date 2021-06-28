"""E_cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls import static

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

# project level imports
from accounts import views as account_views
from products import views as product_views
from orders import views as order_views

router = SimpleRouter()

router.register(r'accounts', account_views.UserViewSet, base_name='accounts')

router.register(r'userroles', account_views.UserRoleViewSet, base_name='userroles')

router.register(r'products',product_views.ProductViewSet,base_name='products')

router.register(r'orders',order_views.OrderViewSet,base_name='orders')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'), namespace='v1')),
]
