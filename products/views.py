from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product
from django.shortcuts import render
from djongo.models import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.db import IntegrityError
from django.http import HttpResponse

# from products.forms import ProductForm


# Create your views here.
#
# class ProductCreateView(TemplateView):
#     template_name = 'products/create-product.html'
#
#     def get(self, request, **kwargs):
#         form = ProductForm
#         return render(request,self.template_name,{'form':form})
#
#     def post(self,request):
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             post.save()
#             form = ProductForm
#             return redirect('products/')
#         args = {'form' : form,}
#         return render(request,self.template_name, args)
# class ProductSaleListView(ListView):
#     template_name = "products/sale-list.html"
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Product.get_products_with_sale()


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


def validate_data_product(posts):
    errors = {}
    if not posts['title']:
        errors['title'] = "This field is required!"
    else:
        if len(posts['title']) < 3:
            errors['title'] = "Len of title must be biggest then 3 characters"
        elif len(posts['title']) > 10:
            errors['title'] = "Len of title must be less then 10 characters"
    if not posts['description']:
        errors['title'] = "This field is required!"
    else:
        if len(posts['description']) > 280:
            errors['description'] = "Len of content must be less then 280 characters"
    try:
        if not posts['price']:
            errors['price'] = "This field is required!"
        else:
            size = int(posts['price'])
            if size <= 0:
                errors['price'] = "Price must be biggest then 0"
    except:
        errors['price'] = "Price must be integer!"
    return errors if errors else None


def create_product(request):
    if request.method == "POST":
        print("ff")
        data = json.loads(request.body)
        errors = validate_data_product(data)
        if not errors:
            post = Product(**data)
            try:
                post.save()
                return HttpResponse(status=201)
            except IntegrityError:
                errors = {'title': "Thing with this name already exists"}
                return HttpResponse(json.dumps(errors), status=400)
        else:
            return HttpResponse(json.dumps(errors), status=400)
    else:
        return render(request, 'products/create-product.html')


def edit_product(request, pk):
    post = Product.get_by_id(pk)
    if request.method == "PUT":
        data = json.loads(request.body)
        errors = validate_data_product(data)
        if not errors:
            product = Product(**data)
            #checking if we changed title
            if post.title == data["title"]:
                product.save()
                return HttpResponse(status=201)
            else:
                try:
                    product.save()
                    return HttpResponse(status=201)
                except IntegrityError:
                    errors = {}
                    errors["title"] = "Product with this title already exists."
                    return HttpResponse(json.dumps(errors), status=400)
        else:
            return HttpResponse(json.dumps(errors), status=400)
    else:
        context = {
            'post': post
        }
        return render(request, 'products/edit-product.html', context)