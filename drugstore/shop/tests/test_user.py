import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .helper import create_user
from .helper import Factory
from .helper import ResponseFilter as rf


class UserTestCase(TestCase):
    url = 'users'

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(slug='simple', is_admin=False)

    # ====================    GET   ==================== #
    def test_get_user_list_not_allowed_status_405(self):
        response = self.client.get(reverse(f'{self.url}-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_valid_user_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user['token'])
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'username': self.user['user'].username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_user_status_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=create_user(slug='admin', is_admin=True)['token'])
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'username': self.user['user'].username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_get_user_status_401(self):
        response = self.client.get(reverse(f'{self.url}-detail', kwargs={'username': self.user['user'].username}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ====================    CREATE    ==================== #
    def create_user(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.post(reverse(f'{self.url}-list'), data=json.dumps(data), content_type='application/json')

    def test_create_valid_user_status_201(self):
        data = Factory.get_user('test')
        response = self.create_user(data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        del data['password']
        self.assertEqual(rf.to_data(response.data), data)

    def test_create_invalid_unique_user_status_400(self):
        response = self.create_user(data=Factory.get_user(slug='simple'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # ====================    UPDATE    ==================== #
    def update_user(self, data, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.put(reverse(f'{self.url}-detail', kwargs={'username': self.user['user'].username}),
                               data=json.dumps(data),
                               content_type='application/json')

    def test_update_valid_user_status_200(self):
        data = Factory.get_user('test')
        response = self.update_user(data=data, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        del data['password']
        self.assertEqual(rf.to_data(response.data), data)

    def test_admin_update_valid_user_status_200(self):
        data = Factory.get_user('test')
        response = self.update_user(data=data, user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        del data['password']
        self.assertEqual(rf.to_data(response.data), data)

    def test_unauthorized_update_user_status_401(self):
        data = Factory.get_user('test')
        response = self.update_user(data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_user_status_403(self):
        data = Factory.get_user('test')
        response = self.update_user(data=data, user=create_user(slug='test1'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ====================    DELETE    ==================== #
    def delete_user(self, username, user=None):
        if user is not None:
            self.client.credentials(HTTP_AUTHORIZATION=user['token'])
        return self.client.delete(reverse(f'{self.url}-detail', kwargs={'username': username}))

    def test_valid_delete_user_status_405(self):
        response = self.delete_user(username=self.user['user'].username, user=create_user(slug='admin', is_admin=True))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_delete_product_group_status_403(self):
        response = self.delete_user(username=self.user['user'].username, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
