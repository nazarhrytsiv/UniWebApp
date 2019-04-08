from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator


# Create your models here.


class ProductManager(models.Manager):

    def sales(self):
        try:
            return Product.objects.filter(sale=True)
        except:
            return None

    def not_sales(self):
        try:
            return Product.objects.filter(sale=False)
        except:
            return None

    def get_by_slug(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except:
            return None

    def get_by_id(self, id):
        qs = Product.objects.filter(id=id)  # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True,unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    image = models.ImageField(upload_to='', null=True, blank=True)
    sale = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        return "/products/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("make-sale-all", kwargs={"id": self.id})

    @staticmethod
    def get_all():
        products = Product.objects.all()
        return products

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
