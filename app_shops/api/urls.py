from django.urls import path

from app_shops.api.views import TopBoughtGoods

urlpatterns = [
    path('top-goods/', TopBoughtGoods.as_view(), name='api top bought goods'),
]