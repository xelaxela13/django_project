from django.contrib.auth import urls
from django.urls import path, include

from users.views import RegistrationView

urlpatterns = [
    path('', include(urls)),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
