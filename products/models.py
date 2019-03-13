from django.db import models


# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    sale = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all():
        products = Product.objects.all()
        return products

    @staticmethod
    def get_by_id(pk):
        try:
            return Product.objects.get(pk=pk)
        except:
            return None

    @staticmethod
    def get_products_with_sale():
        try:
            return Product.objects.filter(sale=True)
        except:
            return None
