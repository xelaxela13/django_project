import csv

from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, TemplateView
from weasyprint import HTML

from products.models import Product


class ProductsView(ListView):
    model = Product


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
