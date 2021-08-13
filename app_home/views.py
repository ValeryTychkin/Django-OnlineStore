from random import randint, sample

from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _

from app_shops.models import DiscountShop, Shop, Goods


class FaviconIco(View):
    """
    GET: На запрос получения favicon.ico возвращает статический файл по (/img/favicon.ico)
    """

    def get(self, request):
        favicon_path = finders.find('img/favicon.ico')
        return HttpResponse(open(favicon_path, 'rb'), content_type="image/ico")


class HomePage(View):
    """
    Обработка запросов к главной странице сайта ('/')
    """

    def get(self, request):
        """
        Используется кэширование случайных объектов из моделей (DiscountShop, Goods)
            и стиль отображения скидок

        :return: Рендер страницы
        """

        random_discounts_view_style = (bool(randint(0, 1)),
                                       bool(randint(0, 1)),
                                       bool(randint(0, 1)))

        discounts_id = list(DiscountShop.objects.values_list('id', flat=True))
        shops_id = list(Shop.objects.values_list('id', flat=True))
        goods_id = list(Goods.objects.values_list('id', flat=True).filter(amount__gt=0))

        random_discounts_id = sample(discounts_id, 3)
        random_shops_id = sample(shops_id, 2)
        random_goods_id = sample(goods_id, 2)

        discounts = DiscountShop.objects.select_related('shop').filter(id__in=random_discounts_id)
        shops = Shop.objects.filter(id__in=random_shops_id)
        goods = Goods.objects.select_related('shop').filter(id__in=random_goods_id)

        context = {
            'title':  _('Home'),
            'discounts': cache.get_or_set('discounts_home_page',  # кэш 10 мин
                                          discounts,
                                          10 * 60),
            'shops': shops,
            'goods': cache.get_or_set('goods_home_page',  # кэш 5 мин
                                      goods,
                                      5 * 60),
            'random_discounts_view': cache.get_or_set('discounts_view_style_home_page',  # кэш 10 мин
                                                      random_discounts_view_style,
                                                      10 * 60),
        }

        return render(request, 'app_home/home_page.html', context)
