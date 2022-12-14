from django.urls import path

from api.products.views import ProductsViewList, ProductsViewRetrieve

urlpatterns = [
    path('products/', ProductsViewList.as_view()),
    path('products/<uuid:pk>/', ProductsViewRetrieve.as_view())
]
