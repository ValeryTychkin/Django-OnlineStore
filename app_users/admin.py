import docutils     # Предотвращает удаления docutils из requirements.txt
                    # если в PyCharm включен «remove unused requirements»

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from app_users import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'username',
                    'amount',
                    'goods_name',
                    'shop_name',
                    'add_time',
                    ]

    def get_queryset(self, request):
        return super(CartAdmin, self).get_queryset(request) \
            .select_related('profile__user',
                            'goods',
                            'goods__shop')

    def username(self, obj):
        return obj.profile.user.username

    username.short_description = _("username")

    def goods_name(self, obj):
        return obj.goods.name

    goods_name.short_description = _("goods name")

    def shop_name(self, obj):
        return obj.goods.shop.name

    shop_name.short_description = _("shop name")


@admin.register(models.ShoppingHistory)
class ShoppingHistoryAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'username',
                    'amount',
                    'goods_name',
                    'shop_name',
                    ]

    def get_queryset(self, request):
        return super(ShoppingHistoryAdmin, self).get_queryset(request) \
                                                .select_related('profile__user',
                                                                'goods',
                                                                'goods__shop')

    def username(self, obj):
        return obj.profile.user.username

    username.short_description = _('username')

    def goods_name(self, obj):
        return obj.goods.name

    goods_name.short_description = _('goods name')

    def shop_name(self, obj):
        return obj.goods.shop.name

    shop_name.short_description = _('shop name')


class ProfileInline(admin.StackedInline):
    model = models.Profile


class CustomUserAdmin(UserAdmin):
    list_display = ['username',
                    'first_name',
                    'last_name',
                    'obj_money_in_account'
                    ]
    inlines = [ProfileInline]

    def obj_money_in_account(self, obj):
        return obj.profile.money_in_account

    obj_money_in_account.short_description = _('money in account')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
