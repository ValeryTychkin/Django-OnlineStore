from rest_framework import serializers

from app_users.models import Cart


class UserCartSerializer(serializers.ModelSerializer):
    goods_cart_id = serializers.IntegerField(source='id')
    goods_name = serializers.CharField(source='goods.name')
    goods_img = serializers.CharField(source='goods.img.url')
    goods_price_with_discount = serializers.FloatField(source='goods.price_with_discount')
    amount_in_stock = serializers.IntegerField(source='goods.amount')
    goods_id = serializers.IntegerField(source='goods.id')
    amount_goods = serializers.IntegerField(source='amount')
    shop_name = serializers.CharField(source='goods.shop.name')

    class Meta:
        model = Cart
        fields = ['goods_cart_id',
                  'amount_goods',
                  'goods_name',
                  'goods_img',
                  'goods_price_with_discount',
                  'amount_in_stock',
                  'goods_id',
                  'shop_name',
                  ]
        read_only_fields = ['goods_cart_id'
                            'goods_img',
                            'goods_price_with_discount',
                            'amount_in_stock',
                            'goods_id',
                            'goods_name',
                            'shop_name',
                            ]
