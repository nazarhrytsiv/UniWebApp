"""UniWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('thing/', include('thing.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from products.views import ProductListView,ProductDetailView,create_product, edit_product, make_sale_all, ProductDetailSlugView, ProductSaleListView,ProductSaleDetailView
from thing.views import create, show_things
from .views import login_page, register_page,logout_page
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', ProductListView.as_view(), name='product-home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('products/', include("products.urls")),
    path('product/create/', create_product),
    # path('sale_all/', make_sale_all, name='make-sale-all'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



