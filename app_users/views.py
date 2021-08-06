from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _

from app_shops.models import DiscountShop
from app_users.forms import RegisterForm, LoginForm, UserPageForm
from app_users.models import Profile, ShoppingHistory, Cart
from app_users.user_profile_processing import UserProfile


class UserPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            id_user = request.user.id
            user_profile_class = UserProfile(Profile.objects.select_related('user')
                                                            .only('user', 'money_in_account', 'amount_spent_money')
                                                            .get(user_id=id_user))
            user_profile = user_profile_class.profile
            user_history = ShoppingHistory.objects.select_related('goods', 'goods__shop') \
                                                  .filter(profile=user_profile) \
                                                  .order_by('-id')[:6]
            shops_discount = DiscountShop.objects.select_related('shop').all().order_by('-id')
            context = {
                'title': user_profile.user.username,
                'user_profile': user_profile,
                'user_history': user_history,
                'user_status': user_profile_class.user_status,
                'user_status_progress': user_profile_class.user_percent_render_progress,
                'shops_discount': cache.get_or_set(f'shops_discount{id_user}',  # кэш 15 мин
                                                   shops_discount,
                                                   0),
                'history_cache_time': 3 * 60,  # кэш 3 мин
            }
            return render(request, 'app_users/user_page.html', context)
        else:
            return redirect('home page')

    def post(self, request):
        """
        :param request: Form POST 'money'= integer
                        Добавляет деньги на аккаунт пользователя отправивший запрос
        """
        try:
            int(request.POST['money'])
            if request.user.is_authenticated:
                user_profile = Profile.objects.only('money_in_account').get(user_id=request.user.id)
                user_profile.money_in_account = float(user_profile.money_in_account) + int(request.POST['money'])
                user_profile.save(update_fields=['money_in_account'])
            return redirect('user')
        except ValueError:
            return redirect('user')


class CartPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_profile = Profile.objects.only('money_in_account').get(user_id=request.user.id)
            context = {
                'title': _('Cart'),
                'goods_list': Cart.objects.select_related('goods', 'goods__shop')
                                          .filter(profile=user_profile)
                                          .order_by('-add_time'),
                'user_profile': user_profile
            }
            return render(request, 'app_users/cart_page.html', context)
        else:
            return redirect('home page')


class ChangeAbout(View):
    def get(self, request):
        if request.user.is_authenticated:
            id_user = request.user.id
            user_profile = Profile.objects.select_related('user').only('user', 'about').get(user_id=id_user)
            user_form = UserPageForm(initial={'f_name': user_profile.user.first_name,
                                              'l_name': user_profile.user.last_name,
                                              'about': user_profile.about,
                                              })
            context = {
                'title': user_profile.user.username,
                'user_obj': user_profile,
                'user_form': user_form,
            }
            return render(request, 'app_users/change_about.html', context)
        else:
            return redirect('home page')

    def post(self, request):
        user_change_form = UserPageForm(request.POST, request.FILES)
        if request.user.is_authenticated:
            id_user = request.user.id
            if user_change_form.is_valid():
                # Сохранение изменений в таблицу User
                user = User.objects.only('first_name', 'last_name').get(id=id_user)
                user.first_name = user_change_form.cleaned_data.get('f_name')
                user.last_name = user_change_form.cleaned_data.get('l_name')
                user.save(update_fields=['first_name', 'last_name'])
                # Сохранение изменений в таблицу Profile
                user_profile = Profile.objects.only('about').get(user_id=id_user)
                user_profile.about = user_change_form.cleaned_data.get('about')
                user_profile.save(update_fields=['about'])
        return redirect('user')


class UserHistory(View):
    def get(self, request):
        if request.user.is_authenticated:
            id_user = request.user.id
            user_profile = Profile.objects.select_related('user').only('user').get(user_id=id_user)
            user_history = ShoppingHistory.objects.select_related('goods', 'goods__shop') \
                                                  .filter(profile=user_profile) \
                                                  .order_by('-id')
            context = {
                'title': _('History') + ' ' + user_profile.user.username,
                'user_history': user_history,
                'cache_time': 5 * 60,  # кэш 5 мин
            }
            return render(request, 'app_users/purchase_history.html', context)
        else:
            return redirect('home page')


class RegisterPage(View):
    def get(self, request):
        context = {
            'title': _('SignUp'),
            'register_form': RegisterForm()
        }
        return render(request, 'app_users/sign_up.html', context)

    def post(self, request):
        user_reg_form = RegisterForm(request.POST)
        if user_reg_form.is_valid():
            # Сохранение нового пользователя
            user = user_reg_form.save()

            user_profile = Profile.objects.only('about').get(user_id=user.id)
            user_profile.about = user_reg_form.cleaned_data.get('about')
            user_profile.save(update_fields=['about'])

            # Аутентификация зарегистрированного пользователя
            username = user_reg_form.cleaned_data.get('username')
            raw_password = user_reg_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home page')
        else:
            context = {
                'title': _('SignUp'),
                'register_form': user_reg_form
            }
            return render(request, 'app_users/sign_up.html', context)


class LoginInOut(View):
    """
        Происходит  верификация пользователей. В зависимости от post['action']: «login» или «logout»
    """
    def post(self, request):
        if request.POST['action'] == 'login':
            user_form = LoginForm(request.POST)
            if user_form.is_valid():
                username = user_form.cleaned_data['username']
                password = user_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect(request.META.get('HTTP_REFERER', ))
                    else:
                        messages.error(request, 'Данная запись не активна')
                else:
                    messages.error(request, 'Логин или Пароль введены не верно')
                return redirect(request.META.get('HTTP_REFERER', ))
        elif request.POST['action'] == 'logout':
            logout(request)
            return redirect(request.META.get('HTTP_REFERER', ))
