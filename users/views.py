from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import CustomAuthenticationForm
from users.model_forms import RegistrationForm


class LoginView(AuthLoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request,
                         f'Welcome back {form.get_user().email}!')
        return super().form_valid(form)


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)
