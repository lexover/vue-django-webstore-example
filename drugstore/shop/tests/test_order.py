import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from shop.models import Order
from shop.models import OrderItem
from shop.models import ShippingAddress
from shop.models import Product
from shop.models import ProductGroup
from shop.models import Country

from shop.serializers import OrderSerializer

from .helper import create_user
from .helper import Factory
from .helper import ResponseFilter as rf


class OrderViewTestCase(TestCase):
    url = 'orders'
    items_count = 3

    def create_order_in_db(self, owner, items_number=3, slug=0):
        order = Order.objects.create(owner=owner)
        country = Country.objects.create(**Factory.get_country(slug))
        product_group = ProductGroup.objects.create(**Factory.get_product_group(slug))
        product = Product.objects.create(**Factory.get_product(group=product_group, slug=slug))
        shipping_address = ShippingAddress.objects.create(**Factory.get_address(order=order, country=country))
        order_items = []
        for num in range(items_number):
            order_items.append(OrderItem.objects.create(
                **Factory.get_order_item(order=order, product=product, slug=slug)))
        return order

    def create_order_json(self, items_number=3, slug=0):
        country = Country.objects.create(**Factory.get_country(slug))
        product_group = ProductGroup.objects.create(**Factory.get_product_group(slug))
        self.product = Product.objects.create(**Factory.get_product(group=product_group, slug=slug))
        items = [Factory.get_order_item(slug=slug, product=self.product.pk) for val in range(items_number)]
        return Factory.get_order(shipping_address=Factory.get_address(country=country.pk), items=items)

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.order = self.create_order_in_db(owner=self.user['user'], slug=1)

    # ====================    GET   ==================== #
    def get_all_orders(self, user=None):
        # Create additional order by anonymous user to check permissions
        self.create_order_in_db(owner=None, slug=2)
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.get(reverse(f'{self.url}-list'))

    def test_get_all_orders_by_anonymous(self):
        response = self.get_all_orders()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rf.to_data(response.data)), 0)

    def test_get_all_orders_by_owner(self):
        response = self.get_all_orders(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rf.to_data(response.data)), 1)

    def test_get_all_orders_by_admin(self):
        response = self.get_all_orders(user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rf.to_data(response.data)), 2)

    def get_order(self, pk, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': pk}))

    def test_get_valid_order_status_200(self):
        response = self.get_order(pk=self.order.pk, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, OrderSerializer(self.order).data)

    def test_get_invalid_order_status_404(self):
        response = self.get_order(pk=self.order.pk+9, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_get_order_status_404(self):
        response = self.get_order(pk=self.order.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ====================    CREATE    ==================== #
    def create_order(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.post(reverse(f'{self.url}-list'), data=json.dumps(data), content_type='application/json')

    def test_create_valid_order_status_201(self):
        data = self.create_order_json(items_number=3, slug=self.items_count + 1)
        response = self.create_order(data=data, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        shipping_address = rf.to_data(response.data['shipping_address'], filters=[rf.filter_order])
        items = [rf.to_data(item, filters=[rf.filter_order]) for item in response.data['order_items']]
        self.assertEqual(shipping_address, data['shipping_address'])
        self.assertEqual(items, data['order_items'])

        subtotal = sum([float(self.product.price) * float(val['quantity']) for val in data['order_items']])
        self.assertAlmostEqual(float(response.data['subtotal']), float(subtotal))

        total = sum([float(self.product.sale_price) * float(val['quantity']) for val in data['order_items']])
        self.assertAlmostEqual(float(response.data['total']), float(total))

    def test_create_invalid_order_status_400(self):
        data = self.create_order_json(items_number=3, slug=self.items_count + 1)
        del data['shipping_address']
        response = self.create_order(data, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ====================    UPDATE    ==================== #
    def update_order(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.put(reverse(f'{self.url}-detail', kwargs={'pk': self.order.pk}),
                               data=json.dumps(data),
                               content_type='application/json')

    def test_update_valid_order_status_200(self):
        data = self.create_order_json(items_number=3, slug=self.items_count + 1)
        response = self.update_order(data=data, user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shipping_address = rf.to_data(response.data['shipping_address'], filters=[rf.filter_order])
        items = [rf.to_data(item, filters=[rf.filter_order]) for item in response.data['order_items']]
        self.assertEqual(shipping_address, data['shipping_address'])
        self.assertEqual(items, data['order_items'])

    def test_update_invalid_order_status_400(self):
        data = self.create_order_json(items_number=3, slug=self.items_count + 1)
        del data['shipping_address']
        response = self.update_order(data=data, user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_update_order_status_404(self):
        data = self.create_order_json(items_number=3, slug=self.items_count + 1)
        response = self.update_order(data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_update_order_status_403(self):
        data = self.create_order_json(items_number=3, slug=self.items_count + 1)
        response = self.update_order(data=data, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ====================    DELETE    ==================== #
    def delete_order(self, pk, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.delete(reverse(f'{self.url}-detail', kwargs={'pk': pk}))

    def test_valid_delete_order_status_204(self):
        response = self.delete_order(pk=self.order.pk, user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_order_status_404(self):
        response = self.delete_order(pk=self.order.pk+9, user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_order_status_404(self):
        response = self.delete_order(pk=self.order.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_order_status_403(self):
        response = self.delete_order(pk=self.order.pk, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
