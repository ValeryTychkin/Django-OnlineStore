from django.test import TestCase
from django.urls import reverse

from app_shops.models import Shop, Goods

MODELS_OBJS_NUM = 5


class ShopListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for shop_num in range(MODELS_OBJS_NUM):
            Shop.objects.create(
                name=f'test_{shop_num}'
            )

    def test_get(self):
        url = reverse('shops list')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shops/shops_list.html')
        self.assertEqual(list(response.context['shops_list']), list(Shop.objects.all().order_by('name')))


class ShopGoodsListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Shop.objects.create(
            name=f'test'
        )
        for goods_num in range(MODELS_OBJS_NUM):
            Goods.objects.create(
                shop=Shop.objects.get(id=1),
                name=goods_num
            )

    def test_get(self):
        url = reverse('shop page', kwargs={'id_shop': 1})
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shops/shop_goods_list.html')
        self.assertEqual(list(response.context['goods_list']), list(Goods.objects.filter(shop_id=1).order_by('name')))


class TopBoughtGoodsTest(TestCase):

    def test_get(self):
        url = reverse('top bought goods')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_shops/top_bought_goods.html')
