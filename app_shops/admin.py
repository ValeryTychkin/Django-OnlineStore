from django.contrib import admin

from app_shops import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'name', 'price']


@admin.register(models.DiscountShop)
class DiscountShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'percentage', 'money']


@admin.register(models.DiscountGoods)
class DiscountGoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'percentage', 'money']
