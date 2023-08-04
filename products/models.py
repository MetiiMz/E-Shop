from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count
from accounts.models import User


class Category(models.Model):
    sub_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategory',
        null=True,
        blank=True
    )
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_filter', args=[self.slug])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    price = models.IntegerField()
    description = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    def rating(self):
        vote = Rating.objects.filter(product=self).aggregate(average=Avg('rate'))
        avg = 0
        if vote['average'] is not None:
            avg = float(vote['average'])
        return avg

    def rate_count(self):
        vote = Rating.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if vote['count'] is not None:
            cnt = int(vote['count'])
        return cnt


class Rating(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='user_rate')
    product = models.ForeignKey(Product, models.CASCADE, related_name='product_rete')
    rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.rate} - {self.product.id}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comment', null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[0:20]} - {self.product}'
