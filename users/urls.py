from django.urls import path, include
from users.views import RegistrationView


urlpatterns = [
    path("accounts/signup/", RegistrationView.as_view(), name="signup"),

    path("accounts/", include("django.contrib.auth.urls")),
]