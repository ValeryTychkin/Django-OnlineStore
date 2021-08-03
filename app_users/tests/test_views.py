from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_shops.models import Shop, DiscountShop, Goods
from app_users.models import Profile

USERS_NUM = 3
SHOPS_NUM = 4
USERS_PASSWORD = 'qaWSed55'


class UserPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(USERS_NUM):
            User.objects.create_user(
                username=f'test{user_num}',
                first_name=f'first_name{user_num}',
                last_name=f'last_name{user_num}',
                password=USERS_PASSWORD
            )
        for shop_num in range(SHOPS_NUM):
            Shop.objects.create(
                name=f'test_{shop_num}'
            )
        for disc_num in range(SHOPS_NUM):
            DiscountShop.objects.create(
                shop=Shop.objects.get(id=1),
                percentage=disc_num
            )
        for goods_num in range(SHOPS_NUM):
            Goods.objects.create(
                shop=Shop.objects.get(id=1),
                name=goods_num
            )

    def test_get(self):
        url = reverse('user')
        response = self.client.get(url, follow=True)

        # Блокировка входа в личный кабинет другого пользователя
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_home/home_page.html')

        user_login = self.client.login(username='test0', password=USERS_PASSWORD)
        response = self.client.get(url, )
        self.assertTrue(user_login)

        # Доступ в свой личный кабинет
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/user_page.html')
        self.assertEqual(response.context['user_profile'].user.id, 1)

    def test_post(self):
        url = reverse('user')

        user_login = self.client.login(username='test0', password=USERS_PASSWORD)
        self.assertTrue(user_login)

        # Подмена числового значения money
        response = self.client.post(url, {'money': 'aaa'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/user_page.html')
        self.assertEqual(float(response.context['user_profile'].money_in_account), 0)

        # Пополнение средств
        response = self.client.post(url, {'money': '150'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/user_page.html')
        self.assertEqual(float(response.context['user_profile'].money_in_account), 150)


class ChangeAboutPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(USERS_NUM):
            User.objects.create_user(
                username=f'test{user_num}',
                first_name=f'first_name{user_num}',
                last_name=f'last_name{user_num}',
                password=USERS_PASSWORD
            )
        for shop_num in range(SHOPS_NUM):
            Shop.objects.create(
                name=f'test_{shop_num}'
            )
        for disc_num in range(SHOPS_NUM):
            DiscountShop.objects.create(
                shop=Shop.objects.get(id=1),
                percentage=disc_num
            )
        for goods_num in range(SHOPS_NUM):
            Goods.objects.create(
                shop=Shop.objects.get(id=1),
                name=goods_num
            )

    def test_get(self):
        url = reverse('change about')
        response = self.client.get(url, follow=True)

        # Блокировка входа на страницу о себе другого пользователя
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_home/home_page.html')

        user_login = self.client.login(username='test0', password=USERS_PASSWORD)
        self.assertTrue(user_login)
        response = self.client.get(url, follow=True)

        # Доступ в на страницу о себе
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/change_about.html')

    def test_post(self):
        url = reverse('change about')

        user_login = self.client.login(username='test0', password=USERS_PASSWORD)
        self.assertTrue(user_login)

        response = self.client.post(url, {'f_name': 'aaa',
                                          'l_name': 'bbb',
                                          'about': 'ccc'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/user_page.html')

        user_profile = Profile.objects.get(user_id=1)
        self.assertEqual(user_profile.user.first_name, 'aaa')
        self.assertEqual(user_profile.user.last_name, 'bbb')
        self.assertEqual(user_profile.about, 'ccc')


class RegisterPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for shop_num in range(SHOPS_NUM):
            Shop.objects.create(
                name=f'test_{shop_num}'
            )
        for disc_num in range(SHOPS_NUM):
            DiscountShop.objects.create(
                shop=Shop.objects.get(id=1),
                percentage=disc_num
            )
        for goods_num in range(SHOPS_NUM):
            Goods.objects.create(
                shop=Shop.objects.get(id=1),
                name=goods_num
            )

    def test_get(self):
        url = reverse('sign-up')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/sign_up.html')

    def test_post(self):
        url = reverse('sign-up')

        response = self.client.post(url, {'username': 'test_reg',
                                          'password1': USERS_PASSWORD,
                                          'password2': USERS_PASSWORD,
                                          'first_name': 'Test',
                                          'last_name': 'Test'},
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)
