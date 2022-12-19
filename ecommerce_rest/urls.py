from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.users.views import Login, Logout

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion API",
      default_version='v0.1',
      description="Documentacion Publica de Ecommerce API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="yordanbb98@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='Login'),
    path('logout', Logout.as_view(), name='Logout'),
    path('usuario/', include('apps.users.api.urls')),
    path('products/', include('apps.products.api.routers')),
]
