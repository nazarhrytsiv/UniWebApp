from django.urls import path, include
from products.views import ProductListView,ProductDetailView,create_product, edit_product, ProductDetailSlugView, ProductSaleListView,ProductSaleDetailView,make_sale_off, make_sale_on


app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view()),
    path('create/', create_product, name='create'),
    path('sale_on/', make_sale_on, name='make-sale-on'),
    path('sale_off/', make_sale_off, name='make_sale_off'),
    path('sale/', ProductSaleListView.as_view(),name='sale'),
    path('sale/<int:pk>/', ProductSaleDetailView.as_view()),
    path('<slug>/', ProductDetailSlugView.as_view()),
    # path('<int:pk>/edit/', edit_product),

    path('<slug>/edit/', edit_product, name='edit'),
]

