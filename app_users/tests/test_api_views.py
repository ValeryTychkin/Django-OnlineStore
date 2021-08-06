from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from app_users.api.serializers import UserCartSerializer
from app_users.models import Cart, Profile, ShoppingHistory
from app_shops.models import Shop, Goods

MODELS_OBJS_NUM = 5
USERNAME = 'user_1'
USERS_PASSWORD = 'qaWSed55'


class UserCartTest(APITestCase):

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            first_name='first_name',
            last_name='last_name',
            password=USERS_PASSWORD
        )
        Shop.objects.create(
            name='shop_1'
        )
        for goods_num in range(MODELS_OBJS_NUM):
            Goods.objects.create(
                shop_id=1,
                name=f'goods_{goods_num}',
                amount=5,
            )
            Cart.objects.create(
                profile_id=1,
                goods_id=goods_num + 1,
                amount=2
            )
        User.objects.create_user(
            username='user_2',
            first_name='first_name',
            last_name='last_name',
            password=USERS_PASSWORD
        )
        Cart.objects.create(
            profile_id=2,
            goods_id=1,
            amount=2
        )

    def test_get(self):
        serialized_data = UserCartSerializer(Cart.objects.select_related('goods', 'goods__shop')
                                                         .filter(profile_id=1)
                                                         .order_by('-add_time'),
                                             many=True).data

        # Проверка пустого возврата при запросе не неверифицированного пользователя
        url = reverse('api user cart')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        # Проверка корректного возврата списка товаров корзины при запросе не верифицированного пользователя
        user_login = self.client.login(username=USERNAME, password=USERS_PASSWORD)
        response = self.client.get(url)

        self.assertTrue(user_login)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_data)

    def test_post(self):
        serialized_data = UserCartSerializer(Cart.objects.select_related('goods', 'goods__shop')
                                                         .filter(profile_id=1)
                                                         .order_by('-add_time'),
                                             many=True).data

        url = reverse('api user cart')

        # Проверка возврата кода статуса ошибки при запросе не неверифицированного пользователя
        response = self.client.post(url, {'goods_cart': serialized_data}, format='json')

        self.assertEqual(response.status_code, 400)

        # Проверка возврата кода статуса ошибки при не верном запросе от верифицированного пользователя
        user_login = self.client.login(username=USERNAME, password=USERS_PASSWORD)
        response = self.client.post(url, {'goods_cart': [{'first': 1, 'second': 2}]}, format='json')

        self.assertTrue(user_login)
        self.assertEqual(response.status_code, 304)

        # Проверка возврата удовлетворительного кода статуса при верном запросе от верифицированного пользователя
        response = self.client.post(url, {'goods_cart': serialized_data}, format='json')

        self.assertEqual(response.status_code, 200)

    def test_change_amount_cart_goods(self):
        serialized_data = UserCartSerializer(Cart.objects.select_related('goods', 'goods__shop')
                                                         .filter(profile_id=1)
                                                         .order_by('-add_time'),
                                             many=True).data
        serialized_data_all_users = UserCartSerializer(Cart.objects.select_related('goods', 'goods__shop')
                                                                   .order_by('-add_time'),
                                                       many=True).data
        serialized_data_all_users[0]['amount_goods'] = 1
        serialized_data_all_users[1]['amount_goods'] = 0

        user_login = self.client.login(username=USERNAME, password=USERS_PASSWORD)
        self.assertTrue(user_login)

        url = reverse('api user cart')

        # Проверка отсутствия изменений корзины при отправки объектов корзины другого пользователя
        self.client.post(url, {'goods_cart': serialized_data_all_users}, format='json')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_data)

        # Проверка принятия изменений корзины при отправки объектов корзины верифицированного пользователя
        serialized_data[0]['amount_goods'] = 1
        serialized_data[1]['amount_goods'] = 0

        response = self.client.post(url, {'goods_cart': serialized_data}, format='json')

        serialized_data.pop(1)

        self.assertEqual(response.status_code, 200)
        response = self.client.get(url)
        self.assertEqual(response.data, serialized_data)


class BuyGoodsTest(APITestCase):

    def setUp(self):
        User.objects.create_user(
            username=USERNAME,
            first_name='first_name',
            last_name='last_name',
            password=USERS_PASSWORD
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
            Cart.objects.create(
                profile_id=1,
                goods_id=goods_num + 1,
                amount=1
            )
        User.objects.create_user(
            username='user_2',
            first_name='first_name',
            last_name='last_name',
            password=USERS_PASSWORD
        )
        Cart.objects.create(
            profile_id=2,
            goods_id=1,
            amount=2
        )

    def test_post(self):
        bought_goods = []
        serialized_data = UserCartSerializer(Cart.objects.select_related('goods', 'goods__shop')
                                             .filter(profile_id=1)
                                             .order_by('-add_time'),
                                             many=True).data
        serialized_data_all_users = UserCartSerializer(Cart.objects.select_related('goods', 'goods__shop')
                                                       .order_by('-add_time'),
                                                       many=True).data

        url = reverse('api buy goods')

        # Проверка возврата кода статуса ошибки при попытки покупки товара неверифицированным пользователем
        response = self.client.post(url, {'goods_buy': serialized_data}, format='json')
        self.assertEqual(response.status_code, 400)

        # Проверка невозможности покупки товара верифицированным пользователем при отсутствия средств
        user_profile = Profile.objects.only('money_in_account').get(id=1)
        user_profile.money_in_account = 10
        user_profile.save(update_fields=['money_in_account'])

        user_login = self.client.login(username=USERNAME, password=USERS_PASSWORD)
        self.assertTrue(user_login)

        response = self.client.post(url, {'goods_buy': serialized_data}, format='json')
        self.assertEqual(response.status_code, 304)
        self.assertEqual(float(Profile.objects.values('money_in_account').get(id=1)['money_in_account']), 10)

        # Проверка невозможности покупки товара верифицированным пользователем
        #          при отсутствии необходимых товаров на складе
        user_profile.money_in_account = 1000
        user_profile.save(update_fields=['money_in_account'])
        serialized_data[0]['amount_goods'] = 2

        response = self.client.post(url, {'goods_buy': serialized_data}, format='json')

        self.assertEqual(response.status_code, 300)
        self.assertEqual(float(Profile.objects.values('money_in_account').get(id=1)['money_in_account']), 1000)
        self.assertEqual(list(ShoppingHistory.objects.all().values_list('goods_id', flat=True)), bought_goods)

        serialized_data[0]['amount_goods'] = 1

        # Проверка невозможности покупки товара верифицированным пользователем другого пользователя
        response = self.client.post(url, {'goods_buy': serialized_data_all_users}, format='json')

        self.assertEqual(response.status_code, 300)
        self.assertEqual(float(Profile.objects.values('money_in_account').get(id=1)['money_in_account']), 1000)
        self.assertEqual(list(ShoppingHistory.objects.all().values_list('goods_id', flat=True)), bought_goods)

        # Проверка успешной покупки товаров верифицированным пользователем
        for goods_num in range(MODELS_OBJS_NUM):
            bought_goods.append(goods_num + 1)

        response = self.client.post(url, {'goods_buy': serialized_data}, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(float(Profile.objects.values('money_in_account').get(id=1)['money_in_account']), 950)
        self.assertEqual(list(ShoppingHistory.objects.all().values_list('goods_id', flat=True)), bought_goods)




