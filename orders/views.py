from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from .forms import CartAddForm
from products.models import Product


class CartView(View):
    def get(self, reqeust):
        cart = Cart(reqeust)
        return render(reqeust, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')
