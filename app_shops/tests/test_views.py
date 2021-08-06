from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_shops.models import Shop, Goods
from app_users.models import Cart

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


class AddGoodsInCart(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='user_1',
            first_name='first_name',
            last_name='last_name',
            password='qaWSed55'
        )
        Shop.objects.create(
            name='shop_1'
        )
        for goods_num in range(MODELS_OBJS_NUM):
            Goods.objects.create(
                shop_id=1,
                name=f'goods_{goods_num}',
                price=10,
                amount=1,
            )

    def test_get(self):
        user_login = self.client.login(username='user_1', password='qaWSed55')
        self.assertTrue(user_login)

        goods_ids_list = list(Goods.objects.values_list('id', flat=True).order_by('id'))

        for goods_num in range(MODELS_OBJS_NUM):  # Добавление товаров в корзину
            url = reverse('add goods in cart', kwargs={'id_goods': goods_num+1})
            self.client.get(url, HTTP_REFERER=reverse('home page'))

        cart_goods_ids_list = list(Cart.objects.select_related('goods')
                                               .values_list('goods_id', flat=True)
                                               .order_by('id'))

        self.assertEqual(goods_ids_list, cart_goods_ids_list)


