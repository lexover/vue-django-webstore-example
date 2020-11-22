import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import ProductGroup
from shop.serializers import ProductGroupSerializer
from shop.views import ProductGroupViewSet

client = Client()

class ProductGroupModelTestCase(TestCase):
    def setUp(self) -> None:
        ProductGroup.objects.create(name="TestGroup_1", description="Description_1")
        ProductGroup.objects.create(name="TestGroup_2", description="Description_2")

    def test_get_one_item_of_product_group(self):
        pg = ProductGroup.objects.get(name="TestGroup_1")
        self.assertEqual(pg.name, "TestGroup_1")
        self.assertEqual(pg.description, "Description_1")

    def test_get_items_list_of_product_group(self):
        pgs = ProductGroup.objects.all()
        self.assertEqual(2, len(pgs))


class ProductGroupViewTestCase(TestCase):
    def setUp(self) -> None:
        self.pg1 = ProductGroup.objects.create(name="TestGroup_1", description="Description_1")
        self.pg2 = ProductGroup.objects.create(name="TestGroup_2", description="Description_2")

    def test_get_all_product_groups_by_factory(self):
        factory = APIRequestFactory()
        view = ProductGroupViewSet.as_view({'get': 'list'})
        # Just to authenticate user
        user = User.objects.create(username='pupkin')

        request = factory.get('product_group')
        # Just to authenticate user
        force_authenticate(request, user=user)
        response = view(request)
        pgs = ProductGroup.objects.all()
        serializer = ProductGroupSerializer(pgs, many=True)
        # Use 'results' because a pager enabled.
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_product_groups(self):
        response = client.get(reverse('productgroup-list'))
        pgs = ProductGroup.objects.all()
        serializer = ProductGroupSerializer(pgs, many=True)
        # Use 'results' because a pager enabled.
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_product_group(self):
        response = client.get(reverse('productgroup-detail', kwargs={'pk': self.pg1.pk}))
        pg = ProductGroup.objects.get(pk=self.pg1.pk)
        serializer = ProductGroupSerializer(pg)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_product_group(self):
        response = client.get(reverse('productgroup-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_product_group(self):
        response = client.post(reverse('productgroup-list'),
                               data=json.dumps({'name': 'TestGroup_3', 'description': 'Description_3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product_group(self):
        # TestGroup_1 already created in __init__ so it have to be BAD_REQUEST
        response = client.post(reverse('productgroup-list'),
                               data=json.dumps({'name': 'TestGroup_1', 'description': 'Description_3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_product_group(self):
        response = client.put(reverse('productgroup-detail', kwargs={'pk': self.pg1.pk}),
                               data=json.dumps({'name': 'TestGroup_3', 'description': 'Description_3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_product_group(self):
        # TestGroup_1 already created in __init__ so it have to be BAD_REQUEST
        response = client.put(reverse('productgroup-detail', kwargs={'pk': self.pg2.pk}),
                               data=json.dumps({'name': 'TestGroup_1', 'description': 'Description_3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_product_group(self):
        response = client.delete(
            reverse('productgroup-detail', kwargs={'pk': self.pg1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product_group(self):
        response = client.delete(
            reverse('productgroup-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AuthorizationTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="User", password="123", first_name="1", last_name="2", email="asd@b.c")

    def test_create_valid_user(self):
        response = client.post(reverse('register'),
                               data=json.dumps({'username': 'User_1', 'password': '123',
                                                'first_name': '1', 'last_name': '2', 'email': 'asd@back.com'}),
                               content_type='application/json')
        self.assertNotEqual(None, response.data.get('token', None))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_email_user(self):
        response = client.post(reverse('register'),
                               data=json.dumps({'username': 'User_1', 'password': '123',
                                                'first_name': '1', 'last_name': '2', 'email': 'asd@back.'}),
                               content_type='application/json')
        self.assertEqual(None, response.data.get('token', None))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_user_already_in_base(self):
        response = client.post(reverse('register'),
                               data=json.dumps({'username': 'User', 'password': '123',
                                                'first_name': '1', 'last_name': '2', 'email': 'asd@back.com'}),
                               content_type='application/json')
        self.assertEqual(None, response.data.get('token', None))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_user(self):
        response = client.post(reverse('login'),
                               data=json.dumps({'username': 'User', 'password': '123'}),
                               content_type='application/json')
        self.assertNotEqual(None, response.data.get('token', None))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user(self):
        response = client.post(reverse('login'),
                               data=json.dumps({'username': 'User_1', 'password': '123'}),
                               content_type='application/json')
        self.assertEqual(None, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_user_auth(self):
        user_token = RefreshToken.for_user(self.user)
        user_token = user_token.access_token
        inner_client = Client(HTTP_AUTHORIZATION=f'Bearer {str(user_token)}')
        response = inner_client.get(reverse('user'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIsNotNone(data.get('token', None))
        del data['token']
        self.assertEqual({'id': 1, 'username': 'User', 'email': 'asd@b.c', 'first_name': '1', 'last_name': '2'}, data)


