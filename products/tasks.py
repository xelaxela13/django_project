import decimal
import io

from django.core.files.images import ImageFile

from products.client.client import products_parser
from products.models import Category, Product
from shop.api_clients import BaseClient
from shop.celery import app


@app.task
def save_parsed_products(products_list: list):
    if not products_list:
        return
    request_client = BaseClient()
    for product_dict in products_list:
        category, _ = Category.objects.get_or_create(
            name=product_dict['category']
        )
        response = request_client.get_request(
            url=product_dict['image'],
            method='get'
        )
        image = ImageFile(io.BytesIO(response), name='image.jpg')
        price = decimal.Decimal(
            ''.join(i for i in product_dict['price'] if i.isdigit())
        )
        product, created = Product.objects.get_or_create(
            name=product_dict['name'],
            category=category,
            defaults={
                'image': image,
                'description': product_dict['description'],
                'sku': product_dict['sku'],
                'price': price
            }
        )
        if not created:
            product.price = price
            product.image = image
            product.save(update_fields=('price', 'image'))


@app.task
def parse_products():
    save_parsed_products.delay(products_parser.parse())
