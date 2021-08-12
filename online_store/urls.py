from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from online_store import settings


schema_view = get_schema_view(
   openapi.Info(
      title="Django–OnlineStore",
      default_version='v1.2.5',
      description="This is web–app create for show «What can I do»",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('i18n', include('django.conf.urls.i18n')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),


    path('', include('app_home.urls')),
    path('shops/', include('app_shops.urls')),
    path('users/', include('app_users.urls')),

    path('api/shops/', include('app_shops.api.urls')),
    path('api/users/', include('app_users.api.urls')),

    path('swagger/', schema_view.with_ui(), name='swagger'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
