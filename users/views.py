from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from users.forms import LoginForm
from users.model_forms import RegistrationForm


# todo remove
class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': kwargs.get('form') or LoginForm})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        form = form(request.POST)
        if form.is_valid():
            login(request, form.user)
        return self.get(request, form=form, *args, **kwargs)


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)
