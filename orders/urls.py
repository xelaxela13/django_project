from django.urls import path

from orders.views import CartView, AddToCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
]
