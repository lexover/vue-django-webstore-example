from enum import Enum
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def create_user(slug='', is_admin=False):
    password = 'password'
    user = User.objects.create_user(username=f'TestUser_{slug}', password=password, is_staff=is_admin)
    token = f'Bearer {RefreshToken.for_user(user).access_token}'
    return {'user': user, 'password': password, 'token': token}


class Factory:
    @staticmethod
    def get_user(slug=''):
        return {
            'username': f'TestUser_{slug}',
            'password': '123456',
            'email': f'email_{slug}@mail.mail',
            'first_name': 'FirstName',
            'last_name': 'LastName'
        }

    @staticmethod
    def get_product_group(slug=0):
        return {
            'name': f'TestGroup_{slug}',
            'description': f'Description_{slug}'
        }

    @staticmethod
    def get_product(group, slug=0):
        return {
            'group': group,
            'name': f'TestProduct_{slug}',
            'image': f'/images/product_01.png',
            'description': f'Description_{slug}',
            'price': f'{float(slug * 10):.2f}',
            'sale': True,
            'sale_price': f'{float(slug * 9):.2f}'
        }

    @staticmethod
    def get_country(slug=0):
        return {
            'name': f'TestCountry_{slug}',
        }

    @staticmethod
    def get_address(country, order=None, slug=0):
        result = {
            'first_name': f'First_name_{slug}',
            'last_name': f'Last_name_{slug}',
            'email': f'name_{slug}@mail.mail',
            'country': country,
            'address': f'1{slug}, Whatever ave.',
            'phone': f'+99999998{slug}',
        }
        if order:
            result['order'] = order
        return result

    @staticmethod
    def get_order_item(product, order=None, slug=0):
        result = {
            'product': product,
            'quantity': 3+slug
        }
        if order:
            result['order'] = order
        return result

    @staticmethod
    def get_order(shipping_address, items):
        return {
            'shipping_address': shipping_address,
            'order_items': items
        }


class ResponseFilter:

    @staticmethod
    def _check_value(data, filters):
        result = {**dict(data)}
        del result['id']
        if filters is not None:
            for filter in filters:
                result = filter(result)
        return result

    # Convert response.data to dictionary which can be compared with data.
    @staticmethod
    def to_data(data, filters=None):
        if 'results' in data:
            result = []
            for value in data.get('results', []):
                result.append(ResponseFilter._check_value(data=value, filters=filters))
            return result
        else:
            return ResponseFilter._check_value(data=data, filters=filters)

    # It fix name of server into the response.
    @staticmethod
    def filter_img(val):
        if 'image' in val:
            img_path = val.get('image', '')
            val['image'] = img_path[img_path.find('/images'):]
        return val

    # It delete hash from file name in response.
    @staticmethod
    def filter_img_hash(val):
        if 'image' in val:
            img_path = val.get('image', '')
            val['image'] = img_path[:img_path.rfind('_')] + img_path[img_path.find('.'):]
        return val

    # Remove from order response order id and programmatically copied values.
    @staticmethod
    def filter_order(val):
        if 'order' in val:
            del val['order']
        if 'price' in val:
            del val['price']
        if 'sale_price' in val:
            del val['sale_price']
        return val
