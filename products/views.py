from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from orders.forms import CartAddForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .forms import CommentForm, CommentReplyForm
from .models import Category, Product, Rating, Comment


class ProductsView(View):
    template_name = 'products/products.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            # To filter the category
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        # Product pagination
        p = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = p.get_page(page)
        return render(request, self.template_name, {
            'categories': categories,
            'page_products': page_products
        })


class ProductDetailView(View):
    form_class = CommentForm
    form_reply_class = CommentReplyForm
    form_cart_add = CartAddForm
    template_name = 'products/product_detail.html'

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product, slug=kwargs['slug'])
        return super().setup(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(is_sub=False)
        comments = self.product_instance.product_comment.filter(is_reply=False)
        return render(
            request,
            self.template_name,
            {
                'product': self.product_instance,
                'categories': categories,
                'comments': comments,
                'form': self.form_class,
                'form_reply': self.form_reply_class,
                'form_cart_add': self.form_cart_add
            }
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # Create a comment
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product_instance
            new_comment.save()
            return redirect('products:product_detail', self.product_instance.slug)


class ProductRateView(LoginRequiredMixin, View):
    def get(self, request, product_id, rate):
        product = get_object_or_404(Product, id=product_id)
        rating = Rating.objects.filter(product=product, user=request.user)
        if rate in range(0, 6):
            if rating.exists():
                rating.delete()
                Rating.objects.create(user=request.user, product=product, rate=rate)
            else:
                Rating.objects.create(user=request.user, product=product, rate=rate)
        else:
            return redirect('products:product_detail', product.slug)
        return redirect('products:product_detail', product.slug)


class ProductCommentReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, product_id, comment_id):
        product = get_object_or_404(Product, id=product_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            reply.save()
        return redirect('products:product_detail', product.slug)
