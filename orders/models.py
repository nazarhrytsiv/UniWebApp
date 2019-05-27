from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from django.urls import reverse

from carts.models import Cart
from UniWebApp.utils import unique_order_id_generator
# Create your models here.

CustomUser = settings.AUTH_USER_MODEL

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid', 'Paid')
)


class OrderManager(models.Manager):

    def new_or_get(self,billing_profile,cart_obj):
        created = False
        qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True, status="created")
        if qs.count() == 1:
            obj = qs.first()
        else:
            created = True
            obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
        return obj, created


class Order(models.Model):
    order_id = models.CharField(max_length=120,blank=True)
    billing_profile = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, default=None,
                                  related_name='User')
    cart = models.ForeignKey(Cart, on_delete='CASCADE')
    status = models.CharField(max_length=120,default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100,decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def get_absolute_url(self, order_id=None):
        return reverse("orders:detail", kwargs={'order_id':order_id})

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = float(cart_total) + float(shipping_total)
        self.total = new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        total = self.total
        if billing_profile is not None and float(total) > 0.0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender,instance,*args, **kwargs):
    cart_obj = instance
    cart_total = cart_obj.total
    cart_id = cart_obj.id
    qs = Order.objects.filter(cart__id=cart_id)
    if qs.exists() == 1:
        order_obj = qs.first()
        order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender,instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)
