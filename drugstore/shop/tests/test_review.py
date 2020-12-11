import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import ProductGroup, Product, Review

from .helper import Factory
from .helper import ResponseFilter as rf
from .helper import create_user


class ReviewTestCase(TestCase):
    url = 'reviews'
    items_number = 3

    def setUp(self) -> None:
        self.client = APIClient()
        product_group = ProductGroup.objects.create(**Factory.get_product_group())
        self.product = Product.objects.create(**Factory.get_product(group=product_group))
        self.user = create_user('test')
        self.instance = Review.objects.create(product=self.product, user=self.user['user'], rating=3, review='test review')
        self.data = {'product': self.product.pk, 'user': self.user['user'].pk, 'rating': 3, 'review': 'test review'}

    # ====================    GET   ==================== #
    def test_get_all_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user['token'])
        response = self.client.get(reverse(f'{self.url}-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(rf.to_data(response.data), [self.data])

    def test_get_valid_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user['token'])
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rf.to_data(response.data), self.data)

    def test_get_invalid_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user['token'])
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ====================    CREATE    ==================== #
    def create_review(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.post(reverse(f'{self.url}-list'), data=json.dumps(data), content_type='application/json')

    def test_create_valid_review_status_201(self):
        user = create_user('test_2')
        data = Factory.get_review(user_id=user['user'].pk, product_id=self.product.pk)
        response = self.create_review(data, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(rf.to_data(response.data), data)

    def test_create_invalid_review_status_400(self):
        self.data['product'] = 999
        response = self.create_review(self.data, create_user(slug='asf', is_admin=False))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_create_review_status_401(self):
        user = create_user('test_2')
        data = Factory.get_review(user_id=user['user'].pk, product_id=self.product.pk)
        response = self.create_review(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ====================    UPDATE    ==================== #
    def update_review(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.put(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk}),
                               data=json.dumps(data), content_type='application/json')

    def test_update_valid_review_status_200(self):
        data = Factory.get_review(user_id=self.user['user'].pk, product_id=self.product.pk, slug=2)
        response = self.update_review(data, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rf.to_data(response.data), data)

    def test_update_invalid_review_status_400(self):
        data = Factory.get_review(user_id=self.user['user'].pk, product_id=100)
        response = self.update_review(data, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_update_review_status_401(self):
        user = create_user('test_2')
        data = Factory.get_review(user_id=user['user'].pk, product_id=self.product.pk, slug=2)
        response = self.update_review(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ====================    DELETE    ==================== #
    def delete_review(self, pk, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.delete(reverse(f'{self.url}-detail', kwargs={'pk': pk}))

    def test_valid_delete_review_status_204(self):
        response = self.delete_review(pk=self.instance.pk, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_review_status_404(self):
        response = self.delete_review(pk=self.instance.pk+1, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_review_status_401(self):
        response = self.delete_review(pk=self.instance.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
