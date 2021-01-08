from functools import reduce

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product
from shop.models import ProductGroup
from shop.models import Review
from .helper import Factory, create_user


class ProductRatingViewTestCase(TestCase):
    url = 'product_rating'
    items_number = 3

    def setUp(self) -> None:
        self.client = APIClient()
        self.group = ProductGroup.objects.create(**Factory.get_product_group())
        self.product = Product.objects.create(**Factory.get_product(group=self.group))
        self.users = [create_user(slug=i, is_admin=False) for i in range(self.items_number)]
        self.data = []
        self.instances = []
        for i in range(self.items_number):
            self.data.append(Factory.get_review(user_id=self.users[i]['user'].pk, product_id=self.product.pk, slug=i))
            self.instances.append(Review.objects.create(**{**self.data[i],
                                                           **{'product': self.product,
                                                              'user': self.users[i]['user']}}))

    def test_get_product_rating_without_search_param_status_404(self):
        response = self.client.get(reverse(f'{self.url}'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 0)

    def test_get_product_rating_with_valid_search_param(self):
        response = self.client.get(reverse(f'{self.url}'), data={'id': self.product.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'value': reduce(lambda r, v: r + v, range(self.items_number)) / self.items_number,
                                         'votes': self.items_number})

    def test_get_empty_product_rating(self):
        product = Product.objects.create(**Factory.get_product(group=self.group, slug=2))
        response = self.client.get(reverse(f'{self.url}'), data={'id': product.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'value': 0, 'votes': 0})

