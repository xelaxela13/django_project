from rest_framework import serializers

from products.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'sku', 'image', 'price',
                  'currency', 'category', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'updated_at')
