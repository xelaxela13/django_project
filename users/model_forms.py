from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
        field_classes = {'email': UsernameField}

    def clean(self):
        self.instance.username = self.cleaned_data['email'].split('@')[0]
        return self.cleaned_data
