"""Колбэки django-unfold: дашборд, бейджи сайдбара, метка окружения."""

import json
from datetime import timedelta

from django.conf import settings
from django.db.models import Count
from django.urls import reverse
from django.utils import formats, timezone

from .filters import day_start
from .models import Categories, FoodEntry, Goods


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


def diary_week(entries):
    """Калории по дням за последние 7 дней (сегодня — последним)."""
    today = timezone.localdate()
    days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    return [
        (
            day,
            entries.filter(
                eaten_at__gte=day_start(day),
                eaten_at__lt=day_start(day + timedelta(days=1)),
            ).totals()["kcal"],
        )
        for day in days
    ]


def dashboard_callback(request, context):
    goods = _scoped(Goods.objects.all(), request)
    categories = _scoped(Categories.objects.all(), request)
    # дневник личный: даже суперпользователь видит только свои записи
    entries = FoodEntry.objects.filter(owner=request.user)

    week = diary_week(entries)
    today_kcal = week[-1][1]
    logged_days = [kcal for _, kcal in week if kcal]
    week_average = round(sum(logged_days) / len(logged_days)) if logged_days else 0
    diary_url = reverse("admin:goodfood_foodentry_changelist")

    kpi = [
        {
            "title": "Сегодня съедено",
            "value": f"{today_kcal} ккал",
            "icon": "local_dining",
            "href": f"{diary_url}?period=today",
        },
        {
            "title": "В среднем за день",
            "value": f"{week_average} ккал",
            "icon": "monitoring",
            "href": f"{diary_url}?period=week",
        },
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
    ]

    week_chart = {
        "labels": [formats.date_format(day, "D, j") for day, _ in week],
        "datasets": [
            {
                "label": "ккал",
                "data": [float(kcal) for _, kcal in week],
                "backgroundColor": "var(--color-primary-500)",
                # у unfold по умолчанию столбики толщиной 4px — для 7 дней мало
                "maxBarThickness": 36,
                "barPercentage": 0.6,
                "borderRadius": 6,
            }
        ],
    }

    today_entries = entries.filter(
        eaten_at__gte=day_start(timezone.localdate())
    ).select_related("goods")
    top_categories = categories.annotate(total=Count("goods")).order_by("-total")[:5]
    max_total = max((c.total for c in top_categories), default=0) or 1

    context.update(
        {
            "kpi": kpi,
            "week_chart": json.dumps(week_chart),
            "today_totals": today_entries.totals(),
            "today_entries": today_entries[:8],
            "diary_add_url": reverse("admin:goodfood_foodentry_add"),
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
