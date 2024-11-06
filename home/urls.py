from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('single_blog/', views.SingleBlogView.as_view(), name='single_blog'),
    path('about/', views.AboutView.as_view(), name='about'),
]
