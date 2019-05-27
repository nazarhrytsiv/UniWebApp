from django.urls import path, include
from orders.views import list_of_orders,detail

app_name = 'orders'

urlpatterns = [
    path('', list_of_orders, name='list'),
    path('<order_id>/', detail, name='detail')
]

