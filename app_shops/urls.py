from django.urls import path

from app_shops.views import ShopPage, ShopsList, AddGoodInCart, TopBoughtGoods

urlpatterns = [
    path('shop-id<int:id_shop>/', ShopPage.as_view(), name='shop page'),
    path('shops-list/', ShopsList.as_view(), name='shops list'),
    path('good-<int:id_goods>/', AddGoodInCart.as_view(), name='add goods in cart'),
    path('top-goods/', TopBoughtGoods.as_view(), name='top bought goods')
]
