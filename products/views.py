from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Product
from django.core.paginator import Paginator


class ProductsView(View):
    template_name = 'products/products.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        p = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = p.get_page(page)
        return render(request, self.template_name, {
            'categories': categories,
            'page_products': page_products
        })


class ProductDetailView(View):
    template_name = 'products/product_detail.html'

    def get(self, request, slug):
        categories = Category.objects.filter(is_sub=False)
        product = get_object_or_404(Product, slug=slug)
        return render(request, self.template_name, {'product': product, 'categories': categories})


