import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product
from shop.models import ProductGroup

from .helper import create_user
from .helper import Factory
from .helper import ResponseFilter as rf


class ProductViewTestCase(TestCase):
    url = 'products'
    items_number = 3

    def setUp(self) -> None:
        self.client = APIClient()
        self.group = ProductGroup.objects.create(**Factory.get_product_group())
        self.data = Factory.get_product(group=self.group.pk)
        self.instance = Product.objects.create(**{**self.data, **{'group': self.group}})
        self.created_images = []

    def tearDown(self) -> None:
        if self.created_images:
            for img in self.created_images:
                os.remove(img)

    # When created product it
    def register_created_image(self, response):
        data = response.data['results'] if 'results' in response.data else response.data
        image_path = data.get('image', None)
        if image_path:
            # Get path from 'images/picture_01.png'
            img = image_path[(image_path.find('/images') + 1):]
            self.created_images.append(os.path.join(settings.MEDIA_ROOT, img))

    # ====================    GET   ==================== #
    def test_get_all_products(self):
        data = [self.data]
        for item in range(1, self.items_number):
            data.append(Factory.get_product(group=self.group.pk, slug=item))
            Product.objects.create(**{**data[item], **{'group': self.group}})

        response = self.client.get(reverse(f'{self.url}-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), self.items_number)
        self.assertEqual(rf.to_data(response.data, filters=[rf.filter_img]), data)

    def test_get_valid_product(self):
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rf.to_data(response.data, filters=[rf.filter_img]), self.data)

    def test_get_invalid_product(self):
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ====================    CREATE    ==================== #
    def create_product(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        with open(os.path.join(settings.MEDIA_ROOT, 'images', 'product_01.png'), 'rb') as image:
            return self.client.post(reverse(f'{self.url}-list'),
                                    data={**data, **{'image': image}},
                                    format='multipart')

    def test_create_valid_product_status_201(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.create_product(data, create_user(is_admin=True))
        self.register_created_image(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(rf.to_data(response.data, filters=[rf.filter_img, rf.filter_img_hash]), data)

    # If sale price is not specified or set to 0.0 it should be replaced in DB by current price.
    def test_create_valid_product_without_sale_price_status_201(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        # Remove 'sale_price' before save.
        del data['sale_price']
        response = self.create_product(data, create_user(is_admin=True))
        self.register_created_image(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Set 'sale_price' as current price before check.
        data['sale_price'] = data['price']
        self.assertEqual(rf.to_data(response.data, filters=[rf.filter_img, rf.filter_img_hash]), data)

    def test_create_invalid_product_status_400(self):
        data = {**Factory.get_product(group=self.group.pk, slug=self.items_number + 1), **{'name': self.data['name']}}
        response = self.create_product(data, create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_create_product_group_status_401(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.create_product(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create_product_group_status_403(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.create_product(data, create_user(is_admin=False))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ====================    UPDATE    ==================== #
    def update_product(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        with open(os.path.join(settings.MEDIA_ROOT, 'images', 'product_01.png'), 'rb') as image:
            return self.client.put(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk}),
                                   data={**data, **{'image': image}},
                                   format='multipart')

    def test_update_valid_product_status_200(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.update_product(data, create_user(is_admin=True))
        self.register_created_image(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rf.to_data(response.data, filters=[rf.filter_img, rf.filter_img_hash]), data)

    def test_update_invalid_product_status_400(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.update_product({**data, **{'name': ''}}, create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_update_product_group_status_401(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.update_product(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_product_group_status_403(self):
        data = Factory.get_product(group=self.group.pk, slug=self.items_number + 1)
        response = self.update_product(data, create_user(is_admin=False))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ====================    DELETE    ==================== #
    def delete_product(self, pk, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.delete(reverse(f'{self.url}-detail', kwargs={'pk': pk}))

    def test_valid_delete_product_status_204(self):
        response = self.delete_product(pk=self.instance.pk, user=create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product_status_404(self):
        response = self.delete_product(pk=self.instance.pk+1, user=create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_product_status_401(self):
        response = self.delete_product(pk=self.instance.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product_status_403(self):
        response = self.delete_product(pk=self.instance.pk, user=create_user())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
