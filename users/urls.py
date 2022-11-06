from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import RegistrationView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
