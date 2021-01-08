from django_filters import rest_framework as django_filters
from django.contrib.auth.models import User

from .models import Product
from .models import Review


# Filter for products by price range and group
class ProductsFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['price', 'min_price', 'max_price', 'group']

# Filter for review by product
class ReviewFilter(django_filters.FilterSet):

    class Meta:
        model = Review
        fields = ['product', 'user']
