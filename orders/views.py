from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView

from orders.mixins import GetCurrentOrderMixin
from orders.forms import AddToCartOrderForm


class CartView(GetCurrentOrderMixin, TemplateView):
    template_name = 'orders/cart.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'current_order': self.get_object()}
        )
        return context


class AddToCartView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('products')

    def post(self, request, *args, **kwargs):
        form = AddToCartOrderForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)
