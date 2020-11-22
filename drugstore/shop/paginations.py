from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class ProductsPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        prices = [float(val['price']) for val in data]
        min_price = min(prices) if len(prices) > 0 else 0
        max_price = max(prices) if len(prices) > 0 else 0
        return Response(OrderedDict([
            ('count', self.count),
            ('min_price', min_price),
            ('max_price', max_price),
            ('results', data)
        ]))
