from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj,new_obj

    def new(self,user=None):
        user_obj = None
        print("in func", user)
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete='CASCADE')
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total_price = 0.0
        for product in products:
            total_price += float(product.price)
        if instance.subtotal != total_price:
            instance.subtotal = total_price
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def m2m_changed_cart_receiver_sale(sender,instance,*args,**kwargs):
    products = instance.products.all()
    price_with_sale = 0.0
    sale = 0.9
    for product in products:
        if product.sale:
            price_with_sale += float(product.price) * sale
        else:
            price_with_sale += float(product.price)
    instance.total = price_with_sale
    instance.save()


m2m_changed.connect(m2m_changed_cart_receiver_sale,sender=Cart.products.through)