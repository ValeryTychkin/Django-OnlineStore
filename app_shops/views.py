from django.shortcuts import render, redirect
from django.utils.formats import get_format
from django.views import View
from django.utils.translation import gettext_lazy as _

from app_shops.models import Shop, Goods
from app_users.models import Profile, Cart


class AddGoodsInCart(View):
    def get(self, request, id_goods):
        if request.user.is_authenticated:
            buyer_profile = Profile.objects.only('id').get(user_id=request.user.id)
            this_goods = Goods.objects.get(id=id_goods)
            if this_goods.amount > 0:
                # Есть ли уже данный товар в корзине ->+  Увеличивает кол. данного товара в корзине пользователя
                if Cart.objects.filter(profile=buyer_profile, goods=this_goods).count() > 0:
                    cart_goods = Cart.objects.get(profile=buyer_profile, goods=this_goods)
                    cart_goods.amount += 1
                    cart_goods.save(update_fields=['amount', 'add_time'])
                else:
                    Cart.objects.create(profile=buyer_profile,
                                        goods=this_goods)
        return redirect(request.META.get('HTTP_REFERER'))


class TopBoughtGoods(View):
    def get(self, request):
        context = {
            'title': _('Top bought goods'),
            'date_format': self.get_html_format_date(),
        }
        return render(request, 'app_shops/top_bought_goods.html', context)

    @staticmethod
    def get_html_format_date():
        """
        :return: HTML формат даты относительно выбранного языка
        """
        date_format = get_format('SHORT_DATE_FORMAT').upper()
        return (date_format[0]*2)+'/'+(date_format[2]*2)+'/'+(date_format[4]*4)


class ShopPage(View):
    def get(self, request, id_shop):
        goods_list = Goods.objects.select_related('shop').filter(shop_id=id_shop).order_by('name')
        context = {
            'title': Shop.objects.get(id=id_shop).name,
            'goods_list': goods_list,
        }
        return render(request, 'app_shops/shop_goods_list.html', context)


class ShopsList(View):
    def get(self, request):
        context = {
            'title': _('Shops'),
            'shops_list': Shop.objects.all().order_by('name'),
        }
        return render(request, 'app_shops/shops_list.html', context)
