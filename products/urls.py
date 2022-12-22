from django.contrib.auth.decorators import login_required
from django.urls import path

from products.views import ProductsView, ProductDetailView, export_csv, \
    ExportPDF, ImportCSV, FavoriteProductsView, \
    FavoriteProductAddOrRemoveView, AJAXFavoriteProductAddOrRemoveView

urlpatterns = [
    path('products/', login_required(ProductsView.as_view()), name='products'),
    path('products/csv/', export_csv, name='export_csv'),
    path('products/import/csv/', ImportCSV.as_view(), name='import_csv'),
    path('products/pdf/', ExportPDF.as_view(), name='export_pdf'),
    path('products/<uuid:pk>/',
         ProductDetailView.as_view(),
         name='product_detail'),
    path('favorites/',
         login_required(FavoriteProductsView.as_view()),
         name='favorites'),
    path('favorites/<uuid:pk>/',
         login_required(FavoriteProductAddOrRemoveView.as_view()),
         name='add_or_remove_favorite'),
    path('ajax-favorites/<uuid:pk>/',
         AJAXFavoriteProductAddOrRemoveView.as_view(),
         name='ajax_add_or_remove_favorite'),
]
