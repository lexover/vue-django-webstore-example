import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product
from shop.models import ProductGroup

from .helper import Factory


class ProductNamesViewTestCase(TestCase):
    url = 'products_names'
    items_number = 5

    def setUp(self) -> None:
        self.client = APIClient()
        self.group = ProductGroup.objects.create(**Factory.get_product_group())
        self.data = []
        self.instances = []
        for item in range(self.items_number):
            self.data.append(Factory.get_product(group=self.group, slug=item))
            self.instances.append(Product.objects.create(**self.data[item]))

    def test_get_product_names_without_search_param(self):
        response = self.client.get(reverse(f'{self.url}'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_product_names_with_short_search_param(self):
        response = self.client.get(reverse(f'{self.url}'), data={'search': 'Te'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_product_names_with_valid_search_param(self):
        response = self.client.get(reverse(f'{self.url}'), data={'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.items_number)

    def test_get_product_names_search_one_value(self):
        response = self.client.get(reverse(f'{self.url}'), data={'search': self.data[self.items_number-1]['name']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_not_allowed(self):
        response = self.client.post(reverse(f'{self.url}'),
                                    data=json.dumps(Factory.get_product(group=self.group.pk, slug=self.items_number + 1)),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
