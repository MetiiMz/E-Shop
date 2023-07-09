from django.shortcuts import render
from django.views import View
from .models import Product


class ProductView(View):
    template_name = 'products/products.html'

    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, self.template_name, {'products': products})
