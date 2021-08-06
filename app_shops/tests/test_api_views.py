from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from rest_framework.test import APITestCase

from app_users.models import ShoppingHistory
from app_shops.models import Shop, Goods
from app_shops.api.serializers import TopBoughtGoodsSerializer

MODELS_OBJS_NUM = 2
USERNAME = 'user_1'
USERS_PASSWORD = 'qaWSed55'


class TopBoughtGoodsTest(APITestCase):

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
                name=f'goods_{goods_num}'
            )
            ShoppingHistory.objects.create(
                profile_id=1,
                goods_id=goods_num + 1,
                amount=goods_num + 1,
                date=f'2021-01-0{goods_num + 1}'
            )

    def test_get(self):
        date_ranges = (('2021-01-01', '2021-01-01'),
                       ('2021-01-02', '2021-01-02'),
                       ('2021-01-01', '2021-01-02'))

        for date_range in date_ranges:
            serialized_data = TopBoughtGoodsSerializer(
                Goods.objects.select_related('shop')
                             .filter(shoppinghistory__date__range=[date_range[0],
                                                                   date_range[1]])
                             .annotate(total_amount=Sum('shoppinghistory__amount'))
                             .order_by('-total_amount'), many=True).data

            url = reverse('api top bought goods')+f'?date_start={date_range[0]}&date_end={date_range[1]}&page=1'
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['results'], serialized_data)

