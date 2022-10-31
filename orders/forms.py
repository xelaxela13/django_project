from django import forms
from django.core.exceptions import ValidationError

from orders.models import Discount
from products.models import Product


class UpdateCartOrderForm(forms.Form):
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

    def save(self, action):
        if action == 'clear':
            self.instance.products.clear()
            return
        elif action == 'pay':
            self.instance.pay()
            return
        getattr(self.instance.products, action)(self.cleaned_data['product'])


class RecalculateCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.fields = {k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                       k != 'csrfmiddlewaretoken'}

    def save(self):
        """
        {'quantity_0': 2,
        'product_0': UUID('e04bc1aa-dc11-4791-a187-5118ea5ce01a'),
        'quantity_1': 2,
        'product_1': UUID('4e26895f-2056-4c57-ad53-3a09c9861b56'),
        'quantity_2': 3,
        'product_2': UUID('f6177123-adb7-4237-bc3e-8a5d2aabae6e')}
        :return: instance
        """
        for k in self.cleaned_data.keys():
            if k.startswith('product_'):
                index = k.split('_')[-1]
                self.instance.products.through.objects \
                    .filter(product_id=self.cleaned_data[f'product_{index}']) \
                    .update(quantity=self.cleaned_data[f'quantity_{index}'])
        return self.instance


class ApplyDiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.order = kwargs['order']

    def clean_code(self):
        try:
            self.instance = Discount.objects.get(
                code=self.cleaned_data['code'],
                is_active=True
            )
        except Discount.DoesNotExist:
            raise ValidationError('Wrong discount code.')
        return self.cleaned_data['code']

    def apply(self):
        self.order.discount = self.instance
        self.order.save(update_fields=('discount',))
