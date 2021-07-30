from django.urls import path

from app_users.api.views import UserCart, BuyGoods


urlpatterns = [
    path('cart/', UserCart.as_view(), name='api user cart'),
    path('buy-goods/', BuyGoods.as_view(), name='api buy goods'),
]
