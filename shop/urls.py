"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.urls import urlpatterns as api_urlpatterns
from feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from main.urls import urlpatterns as main_urlpatterns
from orders.urls import urlpatterns as orders_urlpatterns
from products.urls import urlpatterns as items_urlpatterns
from users.urls import urlpatterns as users_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(items_urlpatterns)),
    path('', include(users_urlpatterns)),
    path('', include(feedbacks_urlpatterns)),
    path('', include(main_urlpatterns)),
    path('', include(orders_urlpatterns)),
    path('api/v1/', include(api_urlpatterns)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
