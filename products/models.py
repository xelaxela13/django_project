import decimal
from os import path

from django.core.cache import cache
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, \
    AFTER_CREATE

from currencies.models import CurrencyHistory
from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/' \
           f'{instance.pk}/image{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.name


class Product(LifecycleModelMixin, PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    products = models.ManyToManyField('products.Product', blank=True)

    _products_cache_key = 'products'

    def __str__(self):
        return f'{self.name} | {self.price} | {self.sku}'

    @property
    def _product_cache_key(self):
        return f'product_{self.id}'

    @classmethod
    def get_products(cls):
        products = cache.get(cls._products_cache_key)
        if not products:
            products = Product.objects.all()
            cache.set(cls._products_cache_key, products)
        return products

    @property
    def exchange_price(self):
        key = self._product_cache_key
        exchange_price = cache.get(key)
        if not exchange_price:
            exchange_price = round(self.price * self.curs, 2)
            cache.set(key, exchange_price)
        return exchange_price

    @property
    def curs(self) -> decimal.Decimal:
        return CurrencyHistory.last_curs(self.currency)

    @hook(AFTER_UPDATE, AFTER_CREATE)
    def order_after_update_or_create(self):
        cache.delete(self._products_cache_key)
        cache.delete(self._product_cache_key)
