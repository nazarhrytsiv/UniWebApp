from django.shortcuts import render, redirect
from .models import Order
from django.contrib.auth.decorators import login_required
# Create your views here.


# @login_required
def list_of_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.all().filter(billing_profile=request.user)
    print(request.user)
    context ={
        "object": orders
    }
    return render(request, "orders/list.html", context)


@login_required()
def detail(request,order_id):
    order = Order.objects.get(order_id=order_id)
    print(order.status)
    context = {
        "object": order
    }
    if request.method == "POST":
        is_done = order.check_done()
        if is_done:
            order.mark_paid()
            return redirect("cart:success")

    return render(request,'orders/detail.html', context)