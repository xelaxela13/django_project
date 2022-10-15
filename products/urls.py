from django.urls import path

from products.views import ProductsView, ProductDetail, export_csv, ExportPDF

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/csv/', export_csv, name='export_csv'),
    path('products/pdf/', ExportPDF.as_view(), name='export_pdf'),
    path('products/<uuid:pk>/', ProductDetail.as_view(),
         name='product_detail'),
]
