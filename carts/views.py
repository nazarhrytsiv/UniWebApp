from django.shortcuts import render
from .models import Cart


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
    total_price = 0.0
    for product in products:
        total_price += float(product.price)
    cart_obj.total = total_price
    cart_obj.save()
    return render(request,'carts/home.html', {})