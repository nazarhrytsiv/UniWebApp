from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product
from carts.models import Cart
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

class ProductSaleListView(ListView):
    template_name = "products/sale-list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.sales()


class ProductSaleDetailView(DetailView):
    template_name = "products/sale-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.sales()


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Cannot get a object")
        return instance


# List of all Products
class ProductListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self):
        request = self.request
        return Product.get_all()


def make_sale_off(request):
    try:
        Product.objects.sales().update(sale=False)
        return redirect('product-home')
    except:
        return HttpResponse(status=301)


def make_sale_on(request):
    try:
        Product.objects.not_sales().update(sale=True)
        return redirect('product-home')
    except:
        return HttpResponse(status=301)


# Detail of single Product
class ProductDetailView(DetailView):
    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
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
        elif len(posts['title']) > 15:
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
            size = float(posts['price'])
            if size <= 0.0:
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


def edit_product(request, slug):
    post = Product.objects.get_by_slug(slug=slug)
    if request.method == "PUT":
        data = json.loads(request.body)
        errors = validate_data_product(data)
        if not errors:
            product = Product(**data)
            # checking if we changed title
            post.title = product.title
            post.description = product.description
            post.price = product.price
            post.sale = product.sale
            post.save()
            return HttpResponse(status=201)
        else:
            return HttpResponse(json.dumps(errors), status=400)
    else:
        context = {
            'post': post
        }
        return render(request, 'products/edit-product.html', context)
