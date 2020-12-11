from django.contrib.auth.models import User, AnonymousUser
from django_filters import rest_framework as django_filters

from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import ProductsFilter

from .models import Country
from .models import Order
from .models import Product
from .models import ProductGroup
from .models import Review

from .permissions import ReadOnly
from .permissions import UserPermission
from .permissions import OrderPermission

from .paginations import ProductsPagination

from .serializers import CountrySerializer
from .serializers import OrderSerializer
from .serializers import ProductGroupSerializer
from .serializers import ProductSerializer
from .serializers import UserSerializer
from .serializers import ReviewSerializer


class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'product_groups': reverse('prodGroups-list', request=request, format=format),
            'products': reverse('products-list', request=request, format=format),
            'products_names': reverse('products_names', request=request, format=format),
            'countries': reverse('countries-list', request=request, format=format),
            'orders': reverse('orders-list', request=request, format=format),
            'check_username': reverse('check_username', request=request, format=format),
            'token_obtain_pair': reverse('token_obtain_pair', request=request, format=format),
            'token_refresh': reverse('token_refresh', request=request, format=format),
        })


# Return list of Product names filtered by 'search' parameter. To use in search input on front-end.
class ProductsNames(APIView):

    def get(self, request):
        search = request.query_params.get('search', None)
        if search and len(search) > 2:
            return Response(Product.objects.values_list('name', flat=True).filter(name__startswith=search))
        return Response(data=[], status=status.HTTP_200_OK)


# Return True of False in accordance is username in 'username' parameter unique (user with such username is not in DB).
class CheckIsUsernameUnique(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [ReadOnly]

    def get(self, request):
        username = request.query_params.get('username', None)
        if username and len(username) > 2:
            result = len(User.objects.filter(username__exact=username)) < 1
            return Response(data=result, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


# View set for product group (categories).
class ProductGroupViewSet(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser | ReadOnly]

    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer


# View set for product countries.
class CountryViewSet(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser | ReadOnly]

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# View set for product countries. It supports search by name, filter by product group (category) and price range,
# ordering by name and price.
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser | ReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductsFilter
    ordering_fields = ['name', 'price']
    search_fields = ['name']
    pagination_class = ProductsPagination

    class Meta:
        ordering = ['-id']


# View set for user. It's not allowed delete operation.
class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [UserPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'


# View set for order. It's complex view set which combine 'order', 'shipping address' and 'order items'.
# Get operation return only orders for which authorized user marked as owner, and all for staff user.
class OrderViewSet(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [OrderPermission]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Overrides get_queryset to restrict the results to only items owned by the authorized user.
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Order.objects.all()
        elif not self.request.user.is_anonymous:
            return Order.objects.all().filter(owner=self.request.user)
        return Order.objects.none()

    # It's necessary to save order owner.
    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            serializer.save(owner=None)
        else:
            serializer.save(owner=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # Overrides get_queryset to restrict the results to only items owned by the authorized user.
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Review.objects.all()
        elif not self.request.user.is_anonymous:
            return Review.objects.all().filter(user=self.request.user)
        return Review.objects.none()

