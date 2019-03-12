from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


# Create your views here.


# List of all Products
class ProductListView(ListView):
    queryset = Product.get_all()
    template_name = "products/list.html"


# Detail of single Product
class ProductDetailView(DetailView):
    queryset = Product.get_all()
    template_name = "products/detail.html"
