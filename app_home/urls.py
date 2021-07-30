from django.urls import path

from app_home.views import HomePage, FaviconIco

urlpatterns = [
    path('', HomePage.as_view(), name='home page'),
    path('favicon.ico', FaviconIco.as_view(), name='favicon'),
]