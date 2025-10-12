from django import forms

from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm

class CustomLoginForm(LoginForm):
    login = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя или Email',
        }),
        label="Логин"
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }),
        label="Пароль"
    )

    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Запомнить меня"
    )
    


class CustomSignupForm(SignupForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
        }),
        label="Имя пользователя"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        }),
        label="Email"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
        }),
        label="Подтвердите пароль"
    )


    



# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(
#         required=True,
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
#     )

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
#         }


# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate, get_user_model

# User = get_user_model()

# class LogInForm(AuthenticationForm):
#     username = forms.CharField(  # Переопределяем стандартное поле username
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Username или Email'
#         })
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Пароль'
#         })
#     )

#     def clean(self):
#         username_or_email = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         if username_or_email and password:
     
#             self.user_cache = authenticate(
#                 self.request,
#                 username=username_or_email,
#                 password=password
#             )

#             # Если не вышло — пробуем по email
#             if self.user_cache is None:
#                 try:
#                     user = User.objects.get(email=username_or_email)
#                     self.user_cache = authenticate(
#                         self.request,
#                         username=user.username,
#                         password=password
#                     )
#                 except User.DoesNotExist:
#                     pass

#             if self.user_cache is None:
#                 raise forms.ValidationError("Неверные данные для входа")

#         return self.cleaned_data

#     def get_user(self):
#         return getattr(self, 'user_cache', None)