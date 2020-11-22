import json
from django.core.management import BaseCommand
from django.db.utils import Error
from shop.models import ProductGroup
from shop.models import Product
from shop.models import Country

class Command(BaseCommand):
    help = 'Delete demo database by demo_db.json specified as argument'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        with open(path, 'rt') as json_file:
            data = json.loads(json_file.read())

            for pr in data['product']:
                try:
                    Product.objects.get(name=pr['name']).delete()
                    print(f'Deleted Product:  {pr}')
                except Error as error:
                    print(f'Product did not deleted: {pr} {error}')

            for pg in data['product_group']:
                ProductGroup.objects.get(name=pg['name']).delete()
                print(f'Deleted Product group:  {pg}')

            for country in data['country']:
                try:
                    Country.objects.get(name=country['name']).delete()
                    print(f'Deleted Country: {country}')
                except Error as error:
                    print(f'Country did not deleted: {country} {error}')
