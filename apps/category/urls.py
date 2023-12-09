from django.urls import path
from .views import *

urlpatterns = [
    path('category',CategoryView.as_view(),name='category'),
    path('items',ItemsView.as_view(),name='item'),
    path('cart',Cartview.as_view(),name='cart'),
    path('orders',OrderView.as_view(),name='orders'),
    path('fav',FavouriteView.as_view(),name='fav'),
    path('payment',PaymentView.as_view(),name='pay')
]
