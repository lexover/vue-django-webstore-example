import json
from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from shop.models import ProductGroup
from shop.models import Product
from shop.models import Country

class Command(BaseCommand):
    help = 'Create demo database from demo_db.json specified as argument'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        with open(path, 'rt') as json_file:
            data = json.loads(json_file.read())

            product_groups = data['product_group']
            for pg in product_groups:
                ProductGroup.objects.get_or_create(name=pg['name'], description=pg['description'])
                print(f'Created Product group:  {pg}')

            products = data['product']
            for pr in products:
                pg = ProductGroup.objects.get(name=pr['group'])
                try:
                    Product.objects.get_or_create(**{**pr, **{'group': pg}})
                    print(f'Created Product:  {pr}')
                except IntegrityError as error:
                    print(f'Product did not created: {pr} {error}')

            countries = data['country']
            for country in countries:
                try:
                    Country.objects.get_or_create(name=country['name'])
                    print(f'Created Country: {country}')
                except IntegrityError as error:
                    print(f'Country did not created: {country} {error}')
