import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView, FormView
from weasyprint import HTML

from products.forms import ImportCSVForm
from products.models import Product


class ProductsView(ListView):
    model = Product

    def get_queryset(self):
        return self.model.get_products()


class ProductDetail(DetailView):
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
