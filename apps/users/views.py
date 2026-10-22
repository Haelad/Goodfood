from urllib.parse import urlencode

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def admin_login(request):
    """Вместо логина unfold — единая страница входа сайта (allauth)."""
    next_url = request.GET.get(REDIRECT_FIELD_NAME, "")
    if not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        next_url = ""

    if request.user.is_authenticated:
        # Обычный пользователь в админку не попадёт — иначе allauth вернёт его
        # обратно по next и получится бесконечный редирект.
        if request.user.is_staff:
            return redirect(next_url or "admin:index")
        return redirect("goodfood:main")

    login_url = reverse("account_login")
    if next_url:
        login_url += "?" + urlencode({REDIRECT_FIELD_NAME: next_url})
    return redirect(login_url)
