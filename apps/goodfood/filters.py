"""Фильтры админки для товаров и дневника питания."""

from datetime import datetime, time, timedelta

from django.utils import timezone
from unfold.contrib.filters.admin import RadioFilter


def day_start(date):
    return timezone.make_aware(datetime.combine(date, time.min))


class PeriodFilter(RadioFilter):
    """Быстрый выбор периода для записей дневника."""

    title = "Период"
    parameter_name = "period"

    def lookups(self, request, model_admin):
        return (
            ("today", "Сегодня"),
            ("yesterday", "Вчера"),
            ("week", "7 дней"),
            ("month", "30 дней"),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()
        ranges = {
            "today": (today, today),
            "yesterday": (today - timedelta(days=1), today - timedelta(days=1)),
            "week": (today - timedelta(days=6), today),
            "month": (today - timedelta(days=29), today),
        }
        if self.value() not in ranges:
            return queryset
        start, end = ranges[self.value()]
        return queryset.filter(
            eaten_at__gte=day_start(start),
            eaten_at__lt=day_start(end + timedelta(days=1)),
        )


class CalorieLevelFilter(RadioFilter):
    """Калорийность на 100 г: грубые группы вместо ввода чисел."""

    title = "Калорийность"
    parameter_name = "kcal_level"

    def lookups(self, request, model_admin):
        return (
            ("low", "Лёгкие — до 150 ккал"),
            ("mid", "Средние — 150–350 ккал"),
            ("high", "Сытные — больше 350 ккал"),
            ("none", "Не указана"),
        )

    def queryset(self, request, queryset):
        match self.value():
            case "low":
                return queryset.filter(kcal__lt=150)
            case "mid":
                return queryset.filter(kcal__gte=150, kcal__lte=350)
            case "high":
                return queryset.filter(kcal__gt=350)
            case "none":
                return queryset.filter(kcal__isnull=True)
        return queryset
