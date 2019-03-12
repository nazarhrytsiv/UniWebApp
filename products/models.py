from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    image = models.ImageField(upload_to='product/', null=True, blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all():
        products = Product.objects.all()
        return products