from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }


class LogInForm(AuthenticationForm):
    login = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username или Email'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def clean(self):
        cleaned_data = super().clean()
        login_input = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login_input and password:
            try:
                user = User.objects.get(username=login_input)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=login_input)
                except User.DoesNotExist:
                    raise forms.ValidationError("Пользователь с таким username или email не найден")

            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
            if not user.is_active:
                raise forms.ValidationError("Пользователь не активен")

            self.user_cache = user

        return self.cleaned_data
    
    def get_user(self):
        return getattr(self, 'user_cache', None)

    