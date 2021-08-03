import os
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('shops')
        verbose_name = _('shop')


def get_upload_path_photo(instance, filename):
    """
    :return: Путь и имя фотографии для товара
        /app_shops/shop_{id магазина}/{имя товара}.{формат фотографии}
    """
    ext = filename.split('.')[-1]
    return os.path.join(
        f'app_shops/shop_{instance.shop.id}/',  # path
        f'{instance.name}.{ext}'  # filename
    )


class Goods(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name=_('shop'))
    name = models.CharField(max_length=150, verbose_name=_('name'))
    img = models.ImageField(upload_to=get_upload_path_photo, default='../static/img/app_shops/tshirt.png')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('price'))
    amount = models.PositiveIntegerField(default=1, verbose_name=_('amount'))

    @property
    def price_with_discount(self):
        """
        Рассчитывает минимальную цену за товар с учетом всех скидок

        :return: Возвращает минимальную цену товара

        Максимальная скидка: 5% от изначальной стоимости товара
        """
        biggest_discounts_shop_dict = self.create_dict_discount(DiscountShop.objects.filter(shop=self.shop))
        biggest_discounts_goods_dict = self.create_dict_discount(DiscountGoods.objects.filter(goods=self))
        return self.price_with_discounts(float(self.price), biggest_discounts_shop_dict, biggest_discounts_goods_dict)

    @staticmethod
    def create_dict_discount(model):
        return {
            'percentage': Goods.check_discount_true(model.order_by('-percentage').first()),
            'money': Goods.check_discount_true(model.order_by('-money').first(), write_in_percentage=False),
        }

    @staticmethod
    def check_discount_true(obj, write_in_percentage=True):
        if obj is None:
            return 0
        else:
            if write_in_percentage:
                return obj.percentage
            return obj.money

    @staticmethod
    def price_with_discounts(price, discounts_shop_dict, discounts_goods_dict):
        """
        :param price: Изначальная цена товара
        :param discounts_shop_dict: Словарь из списка скидок для магазина данного товара
        :param discounts_goods_dict: Словарь из списка скидок для данного товара
        :return: Минимальную цену для данного товара
        """
        min_price = price * 0.05
        new_price = Goods.min_price_discount(price, discounts_shop_dict)
        if new_price > Goods.min_price_discount(price, discounts_goods_dict):
            new_price = Goods.min_price_discount(price, discounts_goods_dict)
        if new_price < min_price:
            new_price = min_price
        if int(new_price) == new_price:
            return int(new_price)
        return Decimal(str(new_price)).quantize(Decimal('0.01'))

    @staticmethod
    def min_price_discount(price, discounts_dict):
        for key, value in discounts_dict.items():
            if key == 'percentage':
                new_price = price * ((100 - value) / 100)
            else:
                new_price = price - value
            if new_price < price:
                price = new_price
        return price

    @property
    def float_price(self):
        return format(float(self.price), '.3g')

    def __str__(self):
        return f'{self.shop} — {self.name} ({self.id})'

    class Meta:
        verbose_name_plural = _('goods')
        verbose_name = _('goods')


class DiscountShop(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, verbose_name=_('shop'))
    is_percentage = models.BooleanField(default=True, verbose_name=_('is percentage'))
    percentage = models.PositiveIntegerField(default=0, verbose_name=_('percentage'))
    money = models.PositiveIntegerField(default=0,  verbose_name=_('money'))

    class Meta:
        verbose_name_plural = _('discounts shops')
        verbose_name = _('discount shop')


class DiscountGoods(models.Model):
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name=_('goods'))
    is_percentage = models.BooleanField(default=True, verbose_name=_('is percentage'))
    percentage = models.PositiveIntegerField(default=0, verbose_name=_('percentage'))
    money = models.PositiveIntegerField(default=0,  verbose_name=_('money'))

    class Meta:
        verbose_name_plural = _('discounts goods')
        verbose_name = _('discount good')
