from django.db import models

from shop.mixins.models_mixins import PKMixin


class Tracking(PKMixin):
    method = models.CharField(max_length=16)
    url = models.CharField(max_length=255)
    data = models.JSONField(default=dict)
