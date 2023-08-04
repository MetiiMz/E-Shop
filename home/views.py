from django.shortcuts import render
from django.views import View
from products.models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': products})


class BlogView(View):
    def get(self, request):
        return render(request, 'home/blog.html')


class SingleBlogView(View):
    def get(self, request):
        return render(request, 'home/single_blog.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')
