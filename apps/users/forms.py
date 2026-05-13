from allauth.account.forms import LoginForm, SignupForm
from django import forms


class CustomLoginForm(LoginForm):
    login = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Имя пользователя или Email",
            }
        ),
        label="Логин",
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Пароль",
            }
        ),
        label="Пароль",
    )

    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Запомнить меня",
    )


class CustomSignupForm(SignupForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Имя пользователя",
            }
        ),
        label="Имя пользователя",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Email",
            }
        ),
        label="Email",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Пароль",
            }
        ),
        label="Пароль",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Подтверждение пароля",
            }
        ),
        label="Подтвердите пароль",
    )
