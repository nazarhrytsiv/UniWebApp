from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


# Create your views here.


# List of all Products
class ProductListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self):
        request = self.request
        return Product.get_all()


# Detail of single Product
class ProductDetailView(DetailView):
    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn`t exist")
        return instance