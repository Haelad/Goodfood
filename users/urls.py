from django.urls import path, include
from django.contrib.auth import views as auth_views

from users.views import login_view, registration_view, exit_view


app_name = "users"



urlpatterns = [
    path("accounts/login/", login_view, name="login"),
    path("accounts/signup/", registration_view, name="signup"),
    path("accounts/exit/", exit_view, name="logout"),

    # сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
