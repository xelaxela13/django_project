from django.db import models

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


class CurrencyHistory(PKMixin):
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )
    curs = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
