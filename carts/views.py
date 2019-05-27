from django.shortcuts import render,redirect
from .models import Cart, Product
from orders.models import Order


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request,'carts/home.html', {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')


def checkout_home(request):
    if not request.user.is_authenticated:
        request.session['cart_items'] = 0
        del request.session['cart_id']
        return redirect("login")
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    if request.user is not None:
        order_obj,order_obj_created = Order.objects.new_or_get(request.user,cart_obj)
        order_obj.save()
    if request.method == "POST":
        "check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")

    context = {
            "object":order_obj,
            "billing_profile":request.user
        }
    return render(request, "carts/checkout.html", context)


def checkout_success(request):
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        return render(request,"carts/success.html", {})