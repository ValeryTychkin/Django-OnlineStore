from rest_framework import serializers

from app_shops.models import Goods


class TopBoughtGoodsSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(source='name')
    goods_img = serializers.CharField(source='img.url')
    goods_price_with_discount = serializers.DecimalField(source='price_with_discount', max_digits=8, decimal_places=2)
    goods_price = serializers.DecimalField(source='price', max_digits=8, decimal_places=2)
    amount_in_stock = serializers.IntegerField(source='amount')
    goods_id = serializers.IntegerField(source='id')
    shop_name = serializers.CharField(source='shop.name')

    class Meta:
        model = Goods
        fields = ['goods_id',
                  'amount_in_stock',
                  'goods_name',
                  'goods_img',
                  'goods_price_with_discount',
                  'goods_price',
                  'shop_name',
                  ]
        read_only_fields = ['goods_id',
                            'amount_in_stock',
                            'goods_name',
                            'goods_img',
                            'goods_price_with_discount',
                            'goods_price',
                            'shop_name',
                            ]
