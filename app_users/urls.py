from django.urls import path

from app_users.views import RegisterPage, LogIn, LogOut, UserPage, ChangeAbout, UserHistory, CartPage

urlpatterns = [
    path('sign-up/', RegisterPage.as_view(), name='sign-up'),
    path('login/', LogIn.as_view(), name='login process'),
    path('logout/', LogOut.as_view(), name='logout process'),
    path('user-page/', UserPage.as_view(), name='user'),
    path('about-user/', ChangeAbout.as_view(), name='change about'),
    path('purchase-history/', UserHistory.as_view(), name='user history'),
    path('user-cart/', CartPage.as_view(), name='user cart'),
]
