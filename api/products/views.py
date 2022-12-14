from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.products.serializers import ProductSerializer, \
    ProductRetrieveSerializer
from products.models import Product


class ProductsViewList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProductsViewRetrieve(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
