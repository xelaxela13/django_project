from django.views.generic import ListView

from products.models import Product


class ProductsView(ListView):
    model = Product
