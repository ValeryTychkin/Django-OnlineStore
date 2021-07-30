from decimal import Decimal

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_shops.models import Goods


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name=_('user'))
    about = models.CharField(max_length=1500, blank=True, verbose_name=_('about'))
    money_in_account = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name=_('money in account'))
    amount_spent_money = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name=_('amount spent money'))

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        """
            Если создается пользователь не через /app_users/full_size/sign_up.html
            то автоматически создается Profile данного пользователя
        """
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')


class ShoppingHistory(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name=_('profile'))
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name=_('goods'))
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_('price'))
    amount = models.PositiveIntegerField(default=1, verbose_name=_('amount'))
    date = models.DateField(default=timezone.now, verbose_name=_('data'))

    class Meta:
        verbose_name_plural = _('shopping history')
        verbose_name = _('shopping history')

    @property
    def total_price(self):
        """
        Общая сума покупки (кол. товаров на цену за один товар: price*amount)
        """
        return self.price * Decimal(str(self.amount))


class Cart(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name=_('profile'))
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name=_('goods'))
    amount = models.PositiveIntegerField(default=1, verbose_name=_('amount'))
    add_time = models.DateTimeField(auto_now=True, verbose_name=_('add time'))

    class Meta:
        verbose_name_plural = _('users cart')
        verbose_name = _('user cart')
