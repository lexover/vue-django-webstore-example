import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Country

from .helper import Factory
from .helper import ResponseFilter as rf
from .helper import create_user


class CountryViewTestCase(TestCase):
    url = 'countries'
    items_number = 3

    def setUp(self) -> None:
        self.client = APIClient()
        self.data = Factory.get_country()
        self.instance = Country.objects.create(**self.data)

    # ====================    GET   ==================== #
    def test_get_all_countries(self):
        data = [self.data]
        for item in range(1, self.items_number):
            data.append(Factory.get_country(item))
            Country.objects.create(**data[item])
        response = self.client.get(reverse(f'{self.url}-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(rf.to_data(response.data), data)

    def test_get_valid_country(self):
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rf.to_data(response.data), self.data)

    def test_get_invalid_country(self):
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ====================    CREATE    ==================== #
    def create_country(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.post(reverse(f'{self.url}-list'), data=json.dumps(data), content_type='application/json')

    def test_create_valid_country_status_201(self):
        data = Factory.get_country(self.items_number + 1)
        response = self.create_country(data, create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(rf.to_data(response.data), data)

    def test_create_invalid_country_status_400(self):
        response = self.create_country(self.data, create_user(is_admin=False))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_create_country_status_401(self):
        data = Factory.get_country(self.items_number + 1)
        response = self.create_country(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create_country_status_403(self):
        data = Factory.get_country(self.items_number + 1)
        response = self.create_country(data, create_user(is_admin=False))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ====================    UPDATE    ==================== #
    def update_country(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.put(reverse(f'{self.url}-detail', kwargs={'pk': self.instance.pk}),
                               data=json.dumps(data), content_type='application/json')

    def test_update_valid_country_status_200(self):
        data = Factory.get_country(self.items_number + 1)
        response = self.update_country(data, create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rf.to_data(response.data), data)

    def test_update_invalid_country_status_400(self):
        data = {**Factory.get_country(self.items_number), **{'name': ''}}
        response = self.update_country(data, create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_update_country_status_401(self):
        data = Factory.get_country(self.items_number + 1)
        response = self.update_country(data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_country_status_403(self):
        data = Factory.get_country(self.items_number + 1)
        response = self.update_country(data, create_user(is_admin=False))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ====================    DELETE    ==================== #
    def delete_country(self, pk, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.delete(reverse(f'{self.url}-detail', kwargs={'pk': pk}))

    def test_valid_delete_country_status_204(self):
        response = self.delete_country(pk=self.instance.pk, user=create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_country_status_404(self):
        response = self.delete_country(pk=self.instance.pk+1, user=create_user(is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_country_status_401(self):
        response = self.delete_country(pk=self.instance.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_country_status_403(self):
        response = self.delete_country(pk=self.instance.pk, user=create_user())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
