from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction

from app_users.models import Cart, Profile, ShoppingHistory
from app_shops.models import Goods
from app_users.api.serializers import UserCartSerializer


class BuyGoods(APIView):
    """
    Представление для покупки товаров путем отправки POST запроса JSON файла — goods_buy: [{goods_1},{goods_2}]
    """

    serializer_class = UserCartSerializer

    @swagger_auto_schema(responses={201: 'Все переданные товары были успешно куплены',
                                    300: 'Переданные данные не валидны',
                                    400: 'Данные пользователя не валидны'})
    def post(self, request):
        """
        :param request: JSON goods_buy: [{goods_1},{goods_2}]
                        Принимает JSON объект c товарами которые хочет купить пользователь
        """
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user_id=request.user.id)
            profile_goods_cart_ids = list(Cart.objects.filter(profile=user_profile)
                                          .order_by('-add_time')
                                          .values_list('id', flat=True))
            profile_goods_cart = Cart.objects.select_related('goods')\
                                             .filter(profile=user_profile)\
                                             .order_by('-add_time')
            data = request.data['goods_buy']
            if isinstance(data, list):
                serializer = self.serializer_class(data=data, many=True)
                if serializer.is_valid():
                    total_cost = 0
                    for goods in serializer.validated_data:
                        # Действительно ли прешедшие товары на изменения, это товары данного пользователя
                        if goods['id'] not in profile_goods_cart_ids:
                            return Response(serializer.errors, status=status.HTTP_300_MULTIPLE_CHOICES)
                        # Есть ли необходимое кол. товара на складе
                        if goods['amount'] > profile_goods_cart.get(id=goods['id']).goods.amount:
                            return Response(serializer.errors, status=status.HTTP_300_MULTIPLE_CHOICES)
                        total_cost += goods['goods']['price_with_discount'] * goods['amount']
                    # Хватает ли пользователю денег для покупки данных товаров
                    if total_cost > float(user_profile.money_in_account):
                        return Response(status=status.HTTP_304_NOT_MODIFIED)
                    self.buy_goods(serializer.validated_data, user_profile, total_cost)
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_304_NOT_MODIFIED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @transaction.atomic
    def buy_goods(validated_data, profile, total_cost):
        """
        Применение изменений в моделях при покупки товара пользователем
        """
        profile.money_in_account = float(profile.money_in_account) - total_cost

        BuyGoods.save_goods_in_history(profile, validated_data)

        # Подсчет общей суммы потраченных денег за все время для записи в поле Profile.amount_spent_money
        user_shopping_history = ShoppingHistory.objects.filter(profile=profile)
        profile.amount_spent_money = sum([b.total_price for b in user_shopping_history])
        profile.save(update_fields=['money_in_account',
                                    'amount_spent_money'])

    @staticmethod
    def save_goods_in_history(profile, validated_data):
        """
        Добавление информации о купленных пользователем товаров в историю покупок
        """
        for goods in validated_data:
            Cart.objects.get(id=goods['id']).delete()

            goods_in_store = Goods.objects.only('amount').get(id=goods['goods']['id'])
            goods_in_store.amount -= goods['amount']
            goods_in_store.save(update_fields=['amount'])

            ShoppingHistory.objects.create(profile=profile,
                                           goods_id=goods['goods']['id'],
                                           price=goods['goods']['price_with_discount'],
                                           amount=goods['amount'])


class UserCart(APIView):
    """
    Представление для получения списка товаров находящиеся в корзине пользователя
    И изменение кол. товаров в корзине путем отправки POST запроса JSON файла — goods_cart: [{goods_1},{goods_2}]
    """

    serializer_class = UserCartSerializer

    def get_queryset(self):
        """
        :return: Объекты модели Cart пользователя отправившим запрос
                 сортировка по времени добавления (по убыванию)
        """
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user_id=self.request.user.id)
            return Cart.objects.select_related('goods', 'goods__shop')\
                               .filter(profile=user_profile)\
                               .order_by('-add_time')

    @swagger_auto_schema(responses={200: serializer_class(many=True)})
    def get(self, request):
        """
        :return: Список товаров в корзине
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: 'Изменения сохранены',
                                    300: 'Переданные данные не валидны',
                                    400: 'Данные пользователя не валидны'})
    def post(self, request):
        """
        :param request: JSON goods_cart: [{goods_1},{goods_2}]
            Принимает JSON объект с измененным кол. товара в корзине покупателя отправившим запрос
            для сохранения изменений
        """
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user_id=request.user.id)
            profile_goods_cart_ids = list(Cart.objects.filter(profile=user_profile)
                                          .order_by('-add_time')
                                          .values_list('id', flat=True))
            data = request.data['goods_cart']

            if isinstance(data, list):
                serializer = self.serializer_class(data=data, many=True)
                if serializer.is_valid():
                    goods_cart_ids = []
                    for goods in serializer.validated_data:
                        goods_cart_ids.append(goods['id'])
                    # Действительно ли прешедшие товары на изменения, это товары данного пользователя
                    if goods_cart_ids != profile_goods_cart_ids:
                        return Response(status=status.HTTP_304_NOT_MODIFIED)
                    self.update_cart_model_goods(serializer.validated_data)
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_304_NOT_MODIFIED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_cart_model_goods(validated_data):
        """
        Сохранение изменений в модели Cart
        """
        for goods in validated_data:
            cart_obj = Cart.objects.get(id=goods['id'])
            if goods['amount'] == 0:
                cart_obj.delete()
            else:
                cart_obj.amount = goods['amount']
                cart_obj.save(update_fields=['amount'])
