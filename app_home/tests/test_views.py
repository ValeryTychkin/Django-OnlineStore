from django.test import TestCase
from django.urls import reverse

from app_shops.models import Shop, DiscountShop, Goods

MODELS_OBJS_NUM = 10


class HomePageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for shop_num in range(MODELS_OBJS_NUM):
            Shop.objects.create(
                name=f'test_{shop_num}'
            )
        for disc_num in range(MODELS_OBJS_NUM):
            DiscountShop.objects.create(
                shop=Shop.objects.get(id=1),
                percentage=disc_num
            )
        for goods_num in range(MODELS_OBJS_NUM):
            Goods.objects.create(
                shop=Shop.objects.get(id=1),
                name=goods_num
            )

    def test_get(self):
        url = reverse('home page')
        response = self.client.get(url, )

        # Проверка срабатывания кэша
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_home/home_page.html')
        discounts = response.context['discounts']
        random_discounts_view = response.context['random_discounts_view']

        response = self.client.get(url, )
        self.assertEqual(list(response.context['discounts']), list(discounts))
        self.assertEqual(response.context['random_discounts_view'], random_discounts_view)
