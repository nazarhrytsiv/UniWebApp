from django.urls import path, include
from products.views import ProductListView,ProductDetailView,create_product, edit_product, make_sale_all, ProductDetailSlugView, ProductSaleListView,ProductSaleDetailView
from thing.views import create, show_things
urlpatterns = [
    path('', ProductListView.as_view()),
      # path('sale_all/', make_sale_all, name='make-sale-all'),
    path('sale/', ProductSaleListView.as_view()),
    path('sale/<int:pk>/', ProductSaleDetailView.as_view()),
    path('<slug>/', ProductDetailSlugView.as_view()),
    # path('product/<int:pk>/', ProductDetailView.as_view()),
    # path('<int:pk>/edit/', edit_product),
    path('<slug>/edit/', edit_product),
]

