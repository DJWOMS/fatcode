from django import forms
from django.contrib.auth.forms import UserCreationForm
from src.profiles.models import FatUser


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = FatUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')

    def clean(self):
        cleaned_data = super().clean()
        if FatUser.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', "Пользователь с таким email уже "
                                           "есть")
        return cleaned_data



