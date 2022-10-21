from django import forms
from django.core.exceptions import ValidationError

from products.models import Product


class AddToCartOrderForm(forms.Form):
    product = forms.UUIDField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']

    def clean_product_id(self):
        try:
            product = Product.objects.get(id=self.cleaned_data['product'])
        except Product.DoesNotExist:
            raise ValidationError('Wrong product id.')
        return product

    def save(self):
        self.instance.products.add(self.cleaned_data['product'])
