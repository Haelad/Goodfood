from django.urls import path, include
from allauth.account import views as allauth_views


urlpatterns = [
    path('accounts/', include('allauth.urls')),

    # path("accounts/login/", allauth_views.LoginView.as_view(), name="account_login"),
    # path("accounts/signup/", allauth_views.SignupView.as_view(), name="account_signup"),
]
