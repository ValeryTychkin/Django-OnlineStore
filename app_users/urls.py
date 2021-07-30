from django.urls import path

from app_users.views import RegisterPage, LoginInOut, UserPage, ChangeAbout, UserHistory, CartPage

urlpatterns = [
    path('sign-up/', RegisterPage.as_view(), name='sign-up'),
    path('log-in-out/', LoginInOut.as_view(), name='log in-out process'),
    path('user-page/', UserPage.as_view(), name='user'),
    path('about-user/', ChangeAbout.as_view(), name='change about'),
    path('purchase-history/', UserHistory.as_view(), name='user history'),
    path('user-cart/', CartPage.as_view(), name='user cart'),
]
