import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import OuterRef, Exists
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView, FormView
from weasyprint import HTML

from products.forms import ImportCSVForm
from products.models import Product, FavoriteProduct


class ProductsView(ListView):
    model = Product

    def get_queryset(self):
        qs = self.model.get_products()
        if self.request.user.is_authenticated:
            sq = FavoriteProduct.objects.filter(
                product=OuterRef('id'),
                user=self.request.user
            )
            qs = qs \
                .prefetch_related('in_favorites') \
                .annotate(is_favorite=Exists(sq))
        return qs


class ProductDetailView(DetailView):
    model = Product


def export_csv(request, *args, **kwargs):
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="products.csv"'},
    )
    fieldnames = ['name', 'description', 'price', 'sku', 'category', 'image']
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for product in Product.objects.iterator():
        writer.writerow(
            {
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'sku': product.sku,
                'category': product.category,
                'image': settings.DOMAIN + product.image.url,
            }
        )
    return response


class ExportPDF(TemplateView):
    template_name = 'products/pdf.html'

    def get(self, request, *args, **kwargs):
        html = loader.render_to_string(
            template_name=self.template_name,
            context=self.get_context_data()
        )
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(
            pdf,
            content_type='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="products.pdf"'
            }
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'products': Product.objects.all(),
                        'domain': settings.DOMAIN})
        return context


class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'products/import_csv.html'
    success_url = reverse_lazy('products')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class FavoriteProductsView(ListView):
    model = FavoriteProduct

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('product', 'user', 'product__category') \
            .prefetch_related('product__products')
        return qs


class FavoriteProductAddOrRemoveView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        favorite, created = FavoriteProduct.objects.get_or_create(
            product=product,
            user=user
        )
        if not created:
            favorite.delete()
        return HttpResponseRedirect(reverse_lazy('products'))
