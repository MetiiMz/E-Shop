from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from .forms import CartAddForm
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem


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


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if request.user == order.user:
            if order.paid is False:
                return render(request, 'orders/order.html', {'order': order})
            else:
                return redirect('accounts:user_profile', request.user.id)
        else:
            return redirect('home:home')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if cart:
            order = Order.objects.create(user=request.user)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return redirect('orders:order_detail', order.id)
        else:
            return redirect('products:products')


class OrderDeleteView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if request.user == order.user:
            if order.paid is False:
                order.delete()
                return redirect('accounts:user_profile', request.user.id)
            else:
                return redirect('accounts:user_profile', request.user.id)
        else:
            return redirect('home:home')


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if request.user == order.user:
            if order.paid is False:
                order.paid = True
                order.save()
                return redirect('accounts:user_profile', request.user.id)
            else:
                return redirect('orders:order_detail', order.id)
        else:
            return redirect('home:home')
