from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import books
from .models import CustomUser


class BookForm(forms.ModelForm):
    class Meta:
        model = books
        fields = ['title', 'author', 'price', 'genre']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Проверяем, передали ли флаг admin через initial
        if not kwargs.get('initial', {}).get('user_is_admin', False):
            self.fields['role'].choices = [
                choice for choice in self.fields['role'].choices if choice[0] != 'admin'
            ]


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
