from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': UsernameField}

    def clean(self):
        self.instance.username = self.cleaned_data['email'].split('@')[0]
        try:
            User.objects.get(username=self.instance.username)
            raise ValidationError("A user with that username already exists.")
        except User.DoesNotExist:
            ...
        return self.cleaned_data
