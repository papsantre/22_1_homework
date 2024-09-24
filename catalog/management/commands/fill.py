import json
from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('catalog.json', 'r', encoding='utf-8') as file:
            categories = json.load(file)
        return categories

    @staticmethod
    def json_read_products():
        with open('catalog2.json', 'r', encoding='utf-8') as file:
            products = json.load(file)
        return products

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    name=category['fields']['name'],
                    description=category['fields']['description'],
                    pk=category['pk'],
                )
            )

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    img_preview=product['fields']['img_preview'],
                    category=Category.objects.get(pk=product['fields']['category']),
                    price=product['fields']['price'],
                    created_at=product['fields']['created_at'],
                    last_modified_date=product['fields']['last_modified_date'],

                    )
            )

        # Создаем объекты продуктов в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)