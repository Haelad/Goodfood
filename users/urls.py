from django.urls import path, include
from users.views import login_view, registration_view, exit_view

app_name = "users"



urlpatterns = [
    path("accounts/login/", login_view, name="login"),
    path("accounts/signup/", registration_view, name="signup"),
    path("accounts/exit/", exit_view, name="logout")
]