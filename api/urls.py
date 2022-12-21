from django.urls import path, include
from rest_framework.authtoken import views

from api.feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from api.products.urls import urlpatterns as products_urlpatterns

urlpatterns = [
    path('', include(products_urlpatterns)),
    path('', include(feedbacks_urlpatterns)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token)
]
