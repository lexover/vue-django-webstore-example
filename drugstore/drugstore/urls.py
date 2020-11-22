"""drugstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from shop import views

router = routers.DefaultRouter()

router.register(r'product_groups', views.ProductGroupViewSet, basename='prodGroups')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'countries', views.CountryViewSet, basename='countries')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('',
         views.ApiRoot.as_view(),
         name='api'),
    path('api-auth/',
         include('rest_framework.urls')),
    path('admin/',
         admin.site.urls,
         name='my_admin/'),
    path('products_names/',
         views.ProductsNames.as_view(),
         name='products_names'),
    path('check_username/',
         views.CheckIsUsernameUnique.as_view(),
         name='check_username'),
    path('token/',
         jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/',
         jwt_views.TokenVerifyView.as_view(),
         name='token_verify'),
    ]
urlpatterns += router.urls

# Register MEDIA_ROOT in urls.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Register Silk plugin, to URL server/silk/
#urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]