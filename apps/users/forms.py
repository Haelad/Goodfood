from allauth.account.forms import LoginForm, SignupForm
from django import forms


class CustomLoginForm(LoginForm):
    login = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Имя пользователя или Email",
            }
        ),
        label="Логин",
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Пароль",
            }
        ),
        label="Пароль",
    )

    remember = forms.BooleanField(
        required=False,
        label="Запомнить меня",
    )


class CustomSignupForm(SignupForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Имя пользователя",
                # как в UnicodeUsernameValidator Django (буквы любого алфавита)
                "pattern": r"[\p{L}\p{N}_.@+\-]+",
                "maxlength": "150",
                "autocomplete": "username",
            }
        ),
        label="Имя пользователя",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
            }
        ),
        label="Email",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # allauth пересоздаёт поля паролей в __init__, поэтому атрибуты — здесь.
        # minlength: MinimumLengthValidator по умолчанию требует 8 символов.
        password_attrs = {
            "minlength": "8",
            "autocomplete": "new-password",
        }
        self.fields["password1"].widget.attrs.update(
            password_attrs, placeholder="Пароль"
        )
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update(
                password_attrs,
                placeholder="Подтверждение пароля",
                # auth-forms.js сверяет значение с полем пароля
                **{"data-match": "id_password1"},
            )
