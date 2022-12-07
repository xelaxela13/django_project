from django.contrib.auth import views as auth_views
from django.urls import path

from users.views import RegistrationView, LoginView, RegistrationConfirmView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/<uidb64>/<token>/confirm/',
         RegistrationConfirmView.as_view(),
         name='registration_confirm'),
]
