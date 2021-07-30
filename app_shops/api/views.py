from django.db.models import Sum
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from app_shops.models import Goods
from app_shops.api.serializers import TopBoughtGoodsSerializer


class TopBoughtGoodsPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 10


class TopBoughtGoods(ListAPIView):
    """
    Представление для получения списка ТОП продаваемых товаров за заданный промежуток времени
    ?date_start=(YYYY-MM-DD)&date_end=(YYYY-MM-DD)&page=(int>0)
    """
    serializer_class = TopBoughtGoodsSerializer
    pagination_class = TopBoughtGoodsPagination

    def get_queryset(self):
        """
        date_start  Начальная дата (включительно)
        date_end    Конечная дата (включительно)
        :return:  Самые продаваемые объекты модели Goods за заданный промежуток времени
        """

        date_start = self.request.query_params.get('date_start', )
        date_end = self.request.query_params.get('date_end', )
        return Goods.objects.select_related('shop')\
                            .filter(shoppinghistory__date__range=[date_start, date_end])\
                            .annotate(total_amount=Sum('shoppinghistory__amount'))\
                            .order_by('-total_amount')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
