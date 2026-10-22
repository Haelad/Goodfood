"""Колбэки django-unfold: дашборд, бейджи сайдбара, метка окружения."""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from .models import Categories, Goods


def _scoped(qs, request):
    """Суперпользователь видит всё, остальные — только свои объекты."""
    if request.user.is_superuser:
        return qs
    return qs.filter(owner=request.user)


def environment_callback(request):
    if settings.DEBUG:
        return ["Разработка", "warning"]
    return ["Продакшн", "danger"]


def goods_badge(request):
    return _scoped(Goods.objects.all(), request).count() or None


def dashboard_callback(request, context):
    goods = _scoped(Goods.objects.all(), request)
    categories = _scoped(Categories.objects.all(), request)
    week_ago = timezone.now() - timedelta(days=7)

    kpi = [
        {
            "title": "Товаров",
            "value": goods.count(),
            "icon": "restaurant_menu",
            "href": reverse("admin:goodfood_goods_changelist"),
        },
        {
            "title": "Категорий",
            "value": categories.count(),
            "icon": "category",
            "href": reverse("admin:goodfood_categories_changelist"),
        },
        {
            "title": "Новых за неделю",
            "value": goods.filter(time_created__gte=week_ago).count(),
            "icon": "fiber_new",
            "href": reverse("admin:goodfood_goods_changelist"),
        },
    ]
    if request.user.is_superuser:
        kpi.append(
            {
                "title": "Пользователей",
                "value": get_user_model().objects.count(),
                "icon": "person",
                "href": reverse("admin:auth_user_changelist"),
            }
        )

    top_categories = categories.annotate(total=Count("goods")).order_by("-total")[:5]
    max_total = max((c.total for c in top_categories), default=0) or 1

    context.update(
        {
            "kpi": kpi,
            "latest_goods": goods.select_related("category")[:5],
            "top_categories": [
                {
                    "title": c.cat,
                    "total": c.total,
                    "percent": round(c.total * 100 / max_total),
                }
                for c in top_categories
            ],
        }
    )
    return context
